"""ISO 21771 / ISO 53 transverse + normal involute gear geometry and 2D contour builders."""

from __future__ import annotations

import math
from typing import Any

try:
    import numpy as np
except ModuleNotFoundError:
    import os as _os
    from pathlib import Path as _Path
    import sys as _sys

    _cp_tag = f"cp{_sys.version_info.major}{_sys.version_info.minor}"
    _orca_roots = [
        _Path(_os.environ["APPDATA"]) / "OrcaSlicer" if _os.environ.get("APPDATA") else None,
        _Path.home() / "Library" / "Application Support" / "OrcaSlicer",
        _Path(_os.environ.get("XDG_CONFIG_HOME") or (_Path.home() / ".config")) / "OrcaSlicer",
    ]
    for _root in _orca_roots:
        if _root is not None:
            _cand = _root / "python" / "packages" / _cp_tag
            if _cand.is_dir() and str(_cand) not in _sys.path:
                _sys.path.insert(0, str(_cand))
    import numpy as np

if "normalize_params" not in globals():
    from .schema import (
        VALID_BORE_TYPES,
        effective_helix_angle_deg,
        normalize_gear_body,
        normalize_params,
    )


def involute_fn(alpha_rad: float) -> float:
    """Standard involute function inv(a) = tan(a) - a (cancellation-free for small angles)."""
    if abs(alpha_rad) < 0.08:
        a2 = alpha_rad * alpha_rad
        a3 = a2 * alpha_rad
        return a3 * (
            (1.0 / 3.0)
            + a2 * (
                (2.0 / 15.0)
                + a2 * ((17.0 / 315.0) + a2 * ((62.0 / 2835.0) + a2 * (1382.0 / 155925.0)))
            )
        )
    return math.tan(alpha_rad) - alpha_rad


def inverse_involute_fn(inv_val: float) -> float:
    """Solve tan(a) - a = inv_val for a in [0, pi/2) via Newton-Raphson accurate to < 1e-14."""
    if not math.isfinite(inv_val) or inv_val <= 0.0:
        return 0.0

    max_alpha = 0.5 * math.pi - 1e-9
    if inv_val < 0.5:
        c = (3.0 * inv_val) ** (1.0 / 3.0)
        alpha = c / (1.0 + 0.4 * c * c / 3.0)
    else:
        alpha = min(max_alpha, 0.5 * math.pi - 1.0 / (inv_val + 0.5 * math.pi))

    alpha = max(1e-15, min(max_alpha, alpha))

    for _ in range(40):
        t = math.tan(alpha)
        t2 = t * t
        if t2 <= 1e-30:
            break
        residual = involute_fn(alpha) - inv_val
        step = residual / t2
        next_alpha = alpha - step
        if next_alpha <= 0.0:
            alpha *= 0.5
        elif next_alpha >= max_alpha:
            alpha = 0.5 * (alpha + max_alpha)
        else:
            alpha = next_alpha
        if abs(step) <= 1e-15:
            break

    return alpha


def _transverse_tooth_thickness_at_radius(
    r: float,
    rb: float,
    psi_b: float,
) -> float:
    """Return transverse arc tooth thickness s_t(r) at radius r >= rb."""
    if r <= 0.0:
        return 0.0
    if r <= rb:
        return 2.0 * r * psi_b
    cos_a = max(-1.0, min(1.0, rb / r))
    alpha_r = math.acos(cos_a)
    psi_r = psi_b - involute_fn(alpha_r)
    return 2.0 * r * psi_r


def _clamp_tip_radius_non_pointed(
    ra_target: float,
    r_ref: float,
    rb: float,
    rf: float,
    psi_b: float,
    min_tip_thickness_mm: float,
) -> tuple[float, float]:
    """Ensure s_t(r_a) >= min_tip_thickness_mm via exact bisection so teeth never self-intersect."""
    s_target = _transverse_tooth_thickness_at_radius(ra_target, rb, psi_b)
    if s_target > min_tip_thickness_mm:
        return ra_target, s_target

    r_lo = max(rf + 0.05, min(r_ref, rb))
    s_lo = _transverse_tooth_thickness_at_radius(r_lo, rb, psi_b)
    if s_lo <= min_tip_thickness_mm:
        return r_lo, max(1e-4, s_lo)

    lo = r_lo
    hi = ra_target
    for _ in range(48):
        mid = 0.5 * (lo + hi)
        s_mid = _transverse_tooth_thickness_at_radius(mid, rb, psi_b)
        if s_mid >= min_tip_thickness_mm:
            lo = mid
        else:
            hi = mid

    s_final = _transverse_tooth_thickness_at_radius(lo, rb, psi_b)
    return lo, max(1e-4, s_final)


def compute_gear_pair_geometry(params: dict[str, Any]) -> dict[str, Any]:
    """Compute ISO 21771 / ISO 53 transverse & normal involute geometry for the gear pair."""
    p = normalize_params(params)

    beta_deg = effective_helix_angle_deg(p)
    beta_rad = math.radians(beta_deg)
    cos_beta = math.cos(beta_rad)

    m_n = float(p["module_mm"])
    m_t = m_n / cos_beta

    alpha_n_deg = float(p["pressure_angle_deg"])
    alpha_n_rad = math.radians(alpha_n_deg)
    tan_alpha_n = math.tan(alpha_n_rad)

    alpha_t_rad = math.atan(tan_alpha_n / cos_beta)
    alpha_t_deg = math.degrees(alpha_t_rad)
    cos_alpha_t = math.cos(alpha_t_rad)
    sin_alpha_t = math.sin(alpha_t_rad)
    inv_alpha_t = involute_fn(alpha_t_rad)

    z1 = int(p["pinion"]["teeth"])
    z2 = int(p["gear"]["teeth"])
    z_sum = float(z1 + z2)

    h_a_coeff = float(p["addendum_coeff"])
    c_coeff = float(p["clearance_coeff"])

    x_min_1 = max(0.0, h_a_coeff - 0.5 * z1 * (sin_alpha_t * sin_alpha_t))
    x_min_2 = max(0.0, h_a_coeff - 0.5 * z2 * (sin_alpha_t * sin_alpha_t))

    raw_x1 = float(p["profile_shift_g1"])
    raw_x2 = float(p["profile_shift_g2"])
    if p["auto_profile_shift"]:
        x1 = max(raw_x1, x_min_1)
        x2 = max(raw_x2, x_min_2)
    else:
        x1 = raw_x1
        x2 = raw_x2

    inv_alpha_tw_raw = inv_alpha_t + 2.0 * tan_alpha_n * (x1 + x2) / z_sum
    alpha_tw_rad = inverse_involute_fn(max(0.0, inv_alpha_tw_raw))
    alpha_tw_deg = math.degrees(alpha_tw_rad)
    cos_alpha_tw = max(1e-6, math.cos(alpha_tw_rad))

    a0 = 0.5 * m_t * z_sum * cos_alpha_t / cos_alpha_tw
    a = max(2.0, a0 + float(p["center_distance_offset_mm"]))

    rw1 = a * float(z1) / z_sum
    rw2 = a * float(z2) / z_sum

    r1 = 0.5 * m_t * float(z1)
    r2 = 0.5 * m_t * float(z2)
    rb1 = r1 * cos_alpha_t
    rb2 = r2 * cos_alpha_t

    backlash_mm = float(p["backlash_mm"])
    xy_comp_mm = float(p["xy_compensation_mm"])
    s_min_pitch = 0.15 * m_t
    s_max_pitch = 0.90 * math.pi * m_t

    s_t1 = m_t * (0.5 * math.pi + 2.0 * x1 * tan_alpha_n) - backlash_mm / (2.0 * cos_beta) - 2.0 * xy_comp_mm
    s_t2 = m_t * (0.5 * math.pi + 2.0 * x2 * tan_alpha_n) - backlash_mm / (2.0 * cos_beta) - 2.0 * xy_comp_mm
    s_t1 = max(s_min_pitch, min(s_max_pitch, s_t1))
    s_t2 = max(s_min_pitch, min(s_max_pitch, s_t2))

    psi_b1 = s_t1 / (2.0 * r1) + inv_alpha_t
    psi_b2 = s_t2 / (2.0 * r2) + inv_alpha_t

    ded1 = max(0.10 * m_n, m_n * (h_a_coeff + c_coeff - x1))
    ded2 = max(0.10 * m_n, m_n * (h_a_coeff + c_coeff - x2))
    rf1 = max(0.8, r1 - ded1)
    rf2 = max(0.8, r2 - ded2)

    add1_raw = max(0.10 * m_n, m_n * (h_a_coeff + x1))
    add2_raw = max(0.10 * m_n, m_n * (h_a_coeff + x2))
    ra1_raw = r1 + add1_raw
    ra2_raw = r2 + add2_raw

    min_tip_s = 0.08 * m_n
    ra1, s_a1 = _clamp_tip_radius_non_pointed(ra1_raw, r1, rb1, rf1, psi_b1, min_tip_s)
    ra2, s_a2 = _clamp_tip_radius_non_pointed(ra2_raw, r2, rb2, rf2, psi_b2, min_tip_s)

    add1 = ra1 - r1
    add2 = ra2 - r2

    # Minimum center distance before zero-backlash dual-flank lockup or tip-to-root bottoming out
    inv_lock_rhs = (float(z1) * psi_b1 + float(z2) * psi_b2 - math.pi) / z_sum
    alpha_lock_rad = inverse_involute_fn(max(0.0, inv_lock_rhs))
    a_inv_lock = (rb1 + rb2) / max(1e-6, math.cos(alpha_lock_rad))
    a_bottom = max(ra1 + rf2, ra2 + rf1)
    min_non_jam_a = max(a_inv_lock, a_bottom)

    pinion_hand = str(p["helix_hand"])
    gear_hand = "left" if pinion_hand == "right" else "right"
    face_w = float(p["face_width_mm"])

    mesh_phase_g2_rad = math.pi - (math.pi / float(z2))
    ratio = float(z2) / float(z1)

    pinion_geom: dict[str, Any] = {
        "teeth": z1,
        "profile_shift": x1,
        "min_profile_shift_no_undercut": x_min_1,
        "undercut": bool(x1 < x_min_1 - 1e-4),
        "pitch_radius_mm": r1,
        "pitch_diameter_mm": 2.0 * r1,
        "working_pitch_radius_mm": rw1,
        "working_pitch_diameter_mm": 2.0 * rw1,
        "base_radius_mm": rb1,
        "base_diameter_mm": 2.0 * rb1,
        "tip_radius_mm": ra1,
        "tip_diameter_mm": 2.0 * ra1,
        "root_radius_mm": rf1,
        "root_diameter_mm": 2.0 * rf1,
        "addendum_mm": add1,
        "dedendum_mm": r1 - rf1,
        "tooth_height_mm": ra1 - rf1,
        "tooth_thickness_pitch_mm": s_t1,
        "tip_thickness_mm": s_a1,
        "base_half_angle_rad": psi_b1,
        "helix_hand": pinion_hand,
        "face_width_mm": face_w,
    }

    gear_geom: dict[str, Any] = {
        "teeth": z2,
        "profile_shift": x2,
        "min_profile_shift_no_undercut": x_min_2,
        "undercut": bool(x2 < x_min_2 - 1e-4),
        "pitch_radius_mm": r2,
        "pitch_diameter_mm": 2.0 * r2,
        "working_pitch_radius_mm": rw2,
        "working_pitch_diameter_mm": 2.0 * rw2,
        "base_radius_mm": rb2,
        "base_diameter_mm": 2.0 * rb2,
        "tip_radius_mm": ra2,
        "tip_diameter_mm": 2.0 * ra2,
        "root_radius_mm": rf2,
        "root_diameter_mm": 2.0 * rf2,
        "addendum_mm": add2,
        "dedendum_mm": r2 - rf2,
        "tooth_height_mm": ra2 - rf2,
        "tooth_thickness_pitch_mm": s_t2,
        "tip_thickness_mm": s_a2,
        "base_half_angle_rad": psi_b2,
        "helix_hand": gear_hand,
        "face_width_mm": face_w,
    }

    return {
        "beta_deg": beta_deg,
        "beta_rad": beta_rad,
        "alpha_n_deg": alpha_n_deg,
        "alpha_t_deg": alpha_t_deg,
        "alpha_tw_deg": alpha_tw_deg,
        "m_n": m_n,
        "m_t": m_t,
        "x1": x1,
        "x2": x2,
        "nominal_center_distance_mm": a0,
        "center_distance_mm": a,
        "min_non_jam_center_distance_mm": min_non_jam_a,
        "ratio": ratio,
        "mesh_phase_g2_rad": mesh_phase_g2_rad,
        "pinion": pinion_geom,
        "gear": gear_geom,
    }


def helix_twist_angle_rad(
    z_mm: float,
    face_width_mm: float,
    pitch_radius_mm: float,
    beta_deg: float,
    hand: str,
    gear_type: str,
) -> float:
    """Compute cross-section axial twist angle psi(z) in radians."""
    gt = str(gear_type).strip().lower()
    if gt == "spur" or abs(beta_deg) < 1e-6 or pitch_radius_mm <= 1e-6:
        return 0.0

    sign = 1.0 if str(hand).strip().lower() == "right" else -1.0
    if gt == "herringbone":
        z_eff = min(float(z_mm), float(face_width_mm) - float(z_mm))
    else:
        z_eff = float(z_mm)

    return sign * z_eff * math.tan(math.radians(float(beta_deg))) / float(pitch_radius_mm)


def build_gear_2d_contour(
    params: dict[str, Any],
    which: str = "pinion",
    samples_per_flank: int = 14,
    radial_inset_mm: float = 0.0,
) -> np.ndarray:
    """Build strictly CCW-ordered (N, 2) float64 array of all Z teeth centered at (0, 0).

    Tooth 0 is centered symmetrically on +X (angle = 0).
    Vertex count is strictly Z * (2 * max(4, samples_per_flank) + 10) regardless of radial_inset_mm
    or tip_chamfer_coeff so Z-rings stitch 1-to-1 without degenerate edges.
    """
    p = normalize_params(params)
    geom = compute_gear_pair_geometry(p)
    key = "gear" if str(which).strip().lower() == "gear" else "pinion"
    g = geom[key]

    z_teeth = int(g["teeth"])
    m_n = float(geom["m_n"])
    m_t = float(geom["m_t"])
    alpha_t_rad = math.radians(float(geom["alpha_t_deg"]))
    alpha_n_rad = math.radians(float(geom["alpha_n_deg"]))
    inv_alpha_t = involute_fn(alpha_t_rad)

    r_ref = float(g["pitch_radius_mm"])
    rb = float(g["base_radius_mm"])
    ra_base = float(g["tip_radius_mm"])
    rf_base = float(g["root_radius_mm"])
    s_t_base = float(g["tooth_thickness_pitch_mm"])

    n_flank = max(4, int(samples_per_flank))
    n_inv = n_flank - 1

    tau_half = math.pi / float(z_teeth)

    # Apply smooth inward bevel offset for anti-elephant-foot chamfer while keeping exact vertex count
    inset = max(0.0, float(radial_inset_mm))
    if inset > 0.0:
        max_safe_inset = min(0.32 * m_n, 0.25 * (ra_base - rf_base), 0.20 * s_t_base)
        eff_inset = min(inset, max(0.0, max_safe_inset))
        rf = max(0.5, rf_base - eff_inset)
        ra_target = max(rf + 0.20 * m_n, ra_base - eff_inset)
        s_t = max(0.16 * m_t, s_t_base - 2.0 * eff_inset / max(0.5, math.cos(alpha_n_rad)))
    else:
        rf = rf_base
        ra_target = ra_base
        s_t = s_t_base

    psi_b = s_t / (2.0 * r_ref) + inv_alpha_t
    ra, _ = _clamp_tip_radius_non_pointed(ra_target, r_ref, rb, rf, psi_b, 0.06 * m_n)

    def _inv_half_angle(radius_val: float) -> float:
        if radius_val <= rb:
            return psi_b
        cos_a = max(-1.0, min(1.0, rb / radius_val))
        return psi_b - involute_fn(math.acos(cos_a))

    # Root fillet join radius & smooth tangent arc to root circle rf
    rho_fillet = max(0.02 * m_n, min(float(p["root_fillet_coeff"]) * m_n, 0.45 * (ra - rf)))
    r_join = max(rb, min(rf + rho_fillet, rf + 0.48 * (ra - rf)))
    r_join = min(r_join, ra - 0.08 * (ra - rf))

    psi_join = _inv_half_angle(r_join)
    # Guarantee root valley angular clearance even on extreme positive profile shift
    max_psi_join = 0.86 * tau_half
    if psi_join > max_psi_join:
        angle_scale = max_psi_join / psi_join
    else:
        angle_scale = 1.0

    def _scaled_psi(radius_val: float) -> float:
        return max(1e-5, _inv_half_angle(radius_val) * angle_scale)

    psi_join_eff = _scaled_psi(r_join)

    # Tip chamfer bevel near r_a
    c_tip_raw = float(p["tip_chamfer_coeff"]) * m_n
    c_tip = max(0.0, min(c_tip_raw, 0.28 * (ra - r_join)))
    psi_ra = _scaled_psi(ra)

    if c_tip > 1e-5:
        r_chamf = ra - c_tip
        psi_tip_corner = max(0.22 * psi_ra, psi_ra - 0.85 * c_tip / max(1.0, ra))
    else:
        # Pure unchamfered involute up to ra with identical vertex count
        r_chamf = r_join + (float(n_inv - 1) / float(n_inv)) * (ra - r_join)
        psi_tip_corner = psi_ra

    # Sample involute flank from r_join to r_chamf with sqrt-biased density near base circle
    u_inv = np.linspace(0.0, 1.0, n_inv, dtype=np.float64)
    # Blend quadratic and linear parameter so base curvature is extra crisp
    s_param = 0.55 * (u_inv * u_inv) + 0.45 * u_inv
    r_inv_pts = r_join + s_param * (r_chamf - r_join)
    psi_inv_pts = np.array([_scaled_psi(float(rv)) for rv in r_inv_pts], dtype=np.float64)

    # Smooth root fillet (3 interior/end samples u in [0.30, 0.65, 1.0]) tangent to root circle rf
    avail_valley = max(1e-4, tau_half - psi_join_eff)
    delta_psi_fil = min(max(rho_fillet / max(1.0, rf), 0.16 * avail_valley), 0.68 * avail_valley)
    psi_fil_end = psi_join_eff + delta_psi_fil

    u_fil = np.array([0.32, 0.68, 1.0], dtype=np.float64)
    psi_fil_upper = psi_join_eff + u_fil * delta_psi_fil
    r_fil_upper = rf + (r_join - rf) * (1.0 - np.sin(0.5 * math.pi * u_fil))

    psi_root_mid = 0.5 * (psi_fil_end + tau_half)

    # Assemble single-tooth polar coordinates (phi, r) in strictly increasing angle order (-tau_half, +tau_half]
    # Count = 1 + 3 + n_flank + 1 + n_flank + 3 + 2 = 2 * n_flank + 10
    phi_lower_flank = np.concatenate((-psi_inv_pts, np.array([-psi_tip_corner], dtype=np.float64)))
    r_lower_flank = np.concatenate((r_inv_pts, np.array([ra], dtype=np.float64)))

    phi_upper_flank = np.concatenate((np.array([psi_tip_corner], dtype=np.float64), psi_inv_pts[::-1]))
    r_upper_flank = np.concatenate((np.array([ra], dtype=np.float64), r_inv_pts[::-1]))

    phi_tooth = np.concatenate(
        (
            np.array([-psi_root_mid], dtype=np.float64),
            -psi_fil_upper[::-1],
            phi_lower_flank,
            np.array([0.0], dtype=np.float64),
            phi_upper_flank,
            psi_fil_upper,
            np.array([psi_root_mid, tau_half], dtype=np.float64),
        )
    )
    r_tooth = np.concatenate(
        (
            np.array([rf], dtype=np.float64),
            r_fil_upper[::-1],
            r_lower_flank,
            np.array([ra], dtype=np.float64),
            r_upper_flank,
            r_fil_upper,
            np.array([rf, rf], dtype=np.float64),
        )
    )

    # Replicate across all Z teeth in vectorized NumPy
    tooth_offsets = (np.arange(z_teeth, dtype=np.float64) * (2.0 * math.pi / float(z_teeth)))[:, None]
    all_angles = (tooth_offsets + phi_tooth[None, :]).reshape(-1)
    all_radii = np.broadcast_to(r_tooth[None, :], (z_teeth, len(r_tooth))).reshape(-1)

    pts = np.empty((len(all_angles), 2), dtype=np.float64)
    pts[:, 0] = all_radii * np.cos(all_angles)
    pts[:, 1] = all_radii * np.sin(all_angles)
    return pts


def _distribute_monotonic_angles(
    critical_angles: list[float],
    total_samples: int,
    interval_weights: list[float] | None = None,
) -> np.ndarray:
    """Distribute `total_samples` strictly increasing angles in [0, 2*pi) hitting every critical corner."""
    two_pi = 2.0 * math.pi
    cleaned: list[float] = []
    for a in sorted(x % two_pi for x in critical_angles):
        if not cleaned or (a - cleaned[-1]) > 1e-5:
            cleaned.append(a)
    if len(cleaned) > 1 and (two_pi + cleaned[0] - cleaned[-1]) <= 1e-5:
        cleaned.pop()
    if not cleaned:
        cleaned = [0.0]

    k = len(cleaned)
    if total_samples <= k:
        return np.linspace(0.0, two_pi, total_samples, endpoint=False, dtype=np.float64)

    spans = [
        (cleaned[(i + 1) % k] - cleaned[i]) % two_pi or two_pi
        for i in range(k)
    ]
    if interval_weights is not None and len(interval_weights) == k:
        weights = [max(1e-4, spans[i] * interval_weights[i]) for i in range(k)]
    else:
        weights = spans

    w_sum = sum(weights)
    raw_counts = [total_samples * (w / w_sum) for w in weights]
    counts = [max(1, int(math.floor(rc))) for rc in raw_counts]

    diff = total_samples - sum(counts)
    if diff > 0:
        remainders = sorted(
            range(k),
            key=lambda idx: (raw_counts[idx] - counts[idx], weights[idx]),
            reverse=True,
        )
        for idx in remainders[:diff]:
            counts[idx] += 1
    elif diff < 0:
        reducibles = sorted(
            range(k),
            key=lambda idx: (counts[idx], -(raw_counts[idx] - counts[idx])),
            reverse=True,
        )
        idx_ptr = 0
        while diff < 0 and idx_ptr < len(reducibles) * 4:
            cand = reducibles[idx_ptr % len(reducibles)]
            if counts[cand] > 1:
                counts[cand] -= 1
                diff += 1
            idx_ptr += 1

    out: list[float] = []
    for i in range(k):
        a0 = cleaned[i]
        span = spans[i]
        c = counts[i]
        for j in range(c):
            out.append((a0 + (float(j) / float(c)) * span) % two_pi)

    # Rotate sequence if cleaned[0] > 0 isn't needed; cleaned[0] == 0.0 keeps strict [0, 2*pi) order
    return np.asarray(out, dtype=np.float64)


def build_bore_2d_contour(
    bore_cfg: dict[str, Any],
    max_allowed_radius_mm: float,
    radial_samples: int = 64,
    extra_clearance_mm: float = 0.0,
) -> np.ndarray | None:
    """Build strictly CCW-ordered (M, 2) float64 closed bore contour, or None if bore_type == 'none'.

    All 5 active bore shapes ('round', 'd_shaft', 'double_d', 'hex', 'keyway') preserve exact
    sharp mechanical corners, strictly monotonic polar angle in [0, 2*pi), fixed length M == radial_samples,
    and outer radius clamped <= max_allowed_radius_mm.
    """
    cfg = normalize_gear_body(bore_cfg if isinstance(bore_cfg, dict) else {})
    bore_type = str(cfg.get("bore_type", "round")).strip().lower()
    if bore_type == "none" or bore_type not in VALID_BORE_TYPES:
        return None

    m_samples = max(18, int(radial_samples))
    max_r = max(0.4, float(max_allowed_radius_mm))

    d_eff = (
        float(cfg["bore_diameter_mm"])
        + float(cfg["bore_clearance_mm"])
        + float(extra_clearance_mm)
    )
    r_nom = max(0.35, min(max_r, 0.5 * d_eff))

    if bore_type == "round":
        angles = np.linspace(0.0, 2.0 * math.pi, m_samples, endpoint=False, dtype=np.float64)
        pts = np.empty((m_samples, 2), dtype=np.float64)
        pts[:, 0] = r_nom * np.cos(angles)
        pts[:, 1] = r_nom * np.sin(angles)
        return pts

    if bore_type in ("d_shaft", "double_d"):
        flat_depth = max(0.05 * r_nom, min(float(cfg["d_flat_depth_mm"]), 0.68 * r_nom))
        y_flat = r_nom - flat_depth
        theta_c = math.asin(max(0.05, min(0.999, y_flat / r_nom)))

        if bore_type == "d_shaft":
            crit = [0.0, theta_c, math.pi - theta_c]
            weights = [1.0, 1.35, 1.0]
        else:
            crit = [0.0, theta_c, math.pi - theta_c, math.pi + theta_c, 2.0 * math.pi - theta_c]
            weights = [1.0, 1.35, 1.0, 1.35, 1.0]

        angles = _distribute_monotonic_angles(crit, m_samples, weights)
        radii = np.full(m_samples, r_nom, dtype=np.float64)
        sin_a = np.sin(angles)
        if bore_type == "d_shaft":
            mask = sin_a > 1e-7
            radii[mask] = np.minimum(r_nom, y_flat / sin_a[mask])
        else:
            abs_sin = np.abs(sin_a)
            mask = abs_sin > 1e-7
            radii[mask] = np.minimum(r_nom, y_flat / abs_sin[mask])

        pts = np.empty((m_samples, 2), dtype=np.float64)
        pts[:, 0] = radii * np.cos(angles)
        pts[:, 1] = radii * sin_a
        return pts

    if bore_type == "hex":
        # Across-flats = 2 * apothem; corner circumradius = apothem / cos(30 deg)
        cos30 = math.cos(math.pi / 6.0)
        apothem = min(r_nom, max_r * cos30)
        crit = [k * (math.pi / 3.0) for k in range(6)]
        angles = _distribute_monotonic_angles(crit, m_samples)
        sector_idx = np.floor((angles % (2.0 * math.pi)) / (math.pi / 3.0)).astype(np.int32)
        sector_idx = np.clip(sector_idx, 0, 5)
        mid_angles = (sector_idx.astype(np.float64) + 0.5) * (math.pi / 3.0)
        radii = np.minimum(max_r, apothem / np.cos(angles - mid_angles))

        pts = np.empty((m_samples, 2), dtype=np.float64)
        pts[:, 0] = radii * np.cos(angles)
        pts[:, 1] = radii * np.sin(angles)
        return pts

    # bore_type == "keyway"
    # Rectangular slot of width keyway_width_mm x radial depth keyway_depth_mm at +Y
    r_circle = min(r_nom, 0.92 * max_r)
    half_w = max(0.15 * r_circle, min(0.5 * float(cfg["keyway_width_mm"]), 0.65 * r_circle))
    y_circle = math.sqrt(max(1e-6, r_circle * r_circle - half_w * half_w))

    max_y_top = math.sqrt(max(y_circle * y_circle + 1e-5, max_r * max_r - half_w * half_w))
    raw_y_top = r_circle + max(0.15, float(cfg["keyway_depth_mm"]))
    y_top = min(raw_y_top, max_y_top)
    if y_top <= y_circle + 0.05:
        # Ultra-tight outer boundary: shrink r_circle slightly so keyway notch stays distinct
        r_circle = max(0.30, 0.80 * max_r)
        half_w = max(0.15 * r_circle, min(0.5 * float(cfg["keyway_width_mm"]), 0.60 * r_circle))
        y_circle = math.sqrt(max(1e-6, r_circle * r_circle - half_w * half_w))
        max_y_top = math.sqrt(max(y_circle * y_circle + 1e-5, max_r * max_r - half_w * half_w))
        y_top = min(r_circle + max(0.15, float(cfg["keyway_depth_mm"])), max_y_top)

    t1 = math.atan2(y_circle, half_w)
    t2 = math.atan2(y_top, half_w)
    t3 = math.pi - t2
    t4 = math.pi - t1

    crit = [0.0, t1, t2, t3, t4]
    weights = [1.0, 2.5, 2.0, 2.5, 1.0]
    angles = _distribute_monotonic_angles(crit, m_samples, weights)

    pts = np.empty((m_samples, 2), dtype=np.float64)
    eps = 1e-9
    for idx, ang in enumerate(angles):
        if t1 - eps <= ang <= t2 + eps:
            x = half_w
            y = min(y_top, max(y_circle, half_w * math.tan(ang)))
        elif t2 - eps < ang < t3 + eps:
            y = y_top
            tan_a = math.tan(ang)
            x = 0.0 if abs(tan_a) > 1e12 else max(-half_w, min(half_w, y_top / tan_a))
        elif t3 - eps <= ang <= t4 + eps:
            x = -half_w
            y = min(y_top, max(y_circle, -half_w * math.tan(ang)))
        else:
            x = r_circle * math.cos(ang)
            y = r_circle * math.sin(ang)
        pts[idx, 0] = x
        pts[idx, 1] = y

    # Final safety radial clamp
    rad_sq = pts[:, 0] * pts[:, 0] + pts[:, 1] * pts[:, 1]
    over_mask = rad_sq > (max_r * max_r)
    if np.any(over_mask):
        scale = max_r / np.sqrt(rad_sq[over_mask])
        pts[over_mask, 0] *= scale
        pts[over_mask, 1] *= scale

    return pts
