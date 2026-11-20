# /// script
# requires-python = ">=3.12"
# dependencies = ["numpy>=1.26"]
#
# [tool.orcaslicer.plugin]
# name = "Orca Gear Studio"
# description = "Estudio parametrico 3D de engrenagens com simulacao de giro, testes de encaixe e envio direto para a mesa"
# author = "Orca Gear Studio"
# version = "1.4.0"
# ///

from __future__ import annotations

import sys as _orca_init_sys
import types as _orca_init_types
if __name__ not in _orca_init_sys.modules:
    _orca_init_sys.modules[__name__] = _orca_init_types.ModuleType(__name__)

# ===========================================================================
# MODULE: gear_studio.locale_catalog
# ===========================================================================

"""Small, offline source-text catalog. Geometry, identifiers and user text are never translated."""
pass  # [bundled] hoisted __future__ import
import re

SUPPORTED_LANGUAGES = ("pt", "en", "es", "it", "fr", "de", "ja")
LANGUAGE_NAMES = ("Português", "English", "Español", "Italiano", "Français", "Deutsch", "日本語")


def normalize_language(value: object, default: str = "pt") -> str:
    raw = str(value or "").strip().lower().split(".", 1)[0].replace("_", "-")
    if not raw:
        return default if default in SUPPORTED_LANGUAGES else "en"
    short = raw.split("-", 1)[0]
    return short if short in SUPPORTED_LANGUAGES else "en"


# One English source and five translations per row; numeric placeholders stay verbatim.
# Kept as readable text in the wheel and source repository, with no online translator.
import base64 as _gear_ui_b64, zlib as _gear_ui_zlib
_GEAR_TRANSLATION_ROWS = _gear_ui_zlib.decompress(_gear_ui_b64.b85decode(b'c-pmnTXPggw(h%rMfzo1Iz|n&@m$z@p9mod%;vf!jJJ82D0OGI%Ifawsfz%)9DyWXz&6G=@C_SdV{;oYHXa)T9!E^S&-o8-T8O9FKjExzt<0*dRtwk>=S0}3D>G|lR$kV9t(@{&)u8Dw=ya^1y*LQ{ARYIj#A~3WbD4_#P^X8ITIWKe;n&md^5yRG&F=EC?(!EydvrAGx9aI+s~&nSo$lnnUQ@T?fD1d9S{hI3A#b*&scGofYH4@z&F<o_y?2gx7hf5gp7m;Rr2a)co6JP%<cm5|M^z=62_hQ6j1GOJRWn#v@YAtyCZt*&)ALcC97&(ojfQTiq*YaWy&2s~SMS{FE?(*`pXx538Jh6DdMk)xzY?YVyK@r{L7G>1&Tsour>mE4ubjCyw4XZDag@?u@5LmFHUIRRZEEf<_(993=gwvNuio(LRC_Q8@uNj^^kH}TN_Xi_cX_$He4M7KGV8UdyM|f|R5f*_bDnC0HSkeY!HcuH*p+H_E~Dbl33Y3rN7PDXLs+?dZsp4x{R4SQO?&e?eM;>}ys+wpDGD0%9{rtcg}UxXaj3bpt<h`PqTly^{j7KGqal9Nz9(<F@8oZo_G67kdLXFMR~<;=*r(qKR+RQtck$!y;?Ld1Z-%DZNw{%mtC~*fN*qM|b0YMqx%nCRv6Sx6p;y)Xv-k7Om22Ow-g%?DeCPfLU#)z7?fwUshMv_8OmND71HVc?C+#ntKHIsBht9VspRUY?oeTAO9WKzWjA=aI@{n!_SOOJ>v{h#U+R+oiOhc<#eqE>Ae4WD_pVjkW(4tkVX}^&}TY9Ct__rL|R4@}@4{qG<$0<E@ZertY9OKnbO)WiFDnYyLo3kUuw7k-emedr@ZQSogQPRReyw+VlD+^0Afsa^P>@F_xnWD9-n#IBj@N!Xa*@AU0M>M68S+m%z*~%?Ck-rWdpfemb{V1Y6h;vEbd?dAne&=S34yc_GDz;6v(pAN)kQN}&d9|%OXX!xG{$HRE;A3l+0^f7*?q?4cKfv)_yw+X(sJrwQZx1?_G$XX-L*63k1U>nx%A15Al2FqlZ4@n=BwL7VpSTOEh7XPu7nMugh2;XfxcpF9U@qxf<bU2he(;}nPYnHM;#cNm!qix+PMf5&*s3RuKvnbp!p`}&Uky@f5TNEso--ACwv>iYeKKo}Vx8s_6&?0lbGo7EytfGdrP*|?UVN{+c>Vs3^D7^{zk2Cf@A@Z0Q+|Cm9(|T@yc*uISxu>pYDZb^rWw#7um+b-Na;?L($**xPLIeT)NbL95uDdqLfS>3y;C={!O)CQ9hFFJ@277tKf86!8P0C0n;J=XF8n$1HEmWd-znu2Bk8o?^0OgLXT>|b1jr7BJF>#vG%ZmdT<W%eL_d9FMs(^XM)ce3uc+z6UR&*_u4uDTo%TXCd}y=!?X?foq4G$ICOccS{IMUZw%_><Ct#xr6OHlqHJq+^%^BaLc0@~PyP;hWdxHT+Iy4Q@E=cs6W>bE=Kx@5GO?g!ndkK(yYfY=}@(11JH@iz$h%!@KgB_RNyLbD-%BfH3!?X7I<O4wv&(bEv-cZBaJvvsQ>U^kD)ohLshNctc(SB{HDxW+xT+5nlv`zHFf@x!$#MDIRZJza#SSKO&J(>s*6l5*H5zKae#5!*G<_aCq2Xq(Dbr;{Iq2K#;Y31|{TZi%QoZhFVW7<T7-PGpNrcIp>Q<Tx>B|1u_ZecW_;h?fX09P)3ymI@DDIp}{%^#(9$&A`m`u#K1Mlh4A1YsP|^34#U4zfC~3jG<v*52T1dNB#nNVjT1Sm|8WwswjeYqcv07Yy0~!ZfuHu71?J`%~}sH}`&dn`X)s4?Roksm6m=OcPCGF5@d`r2^`P%K}?C+0gSmBtm%Y&}V{U>vn`VoP=}Q^ifzmdbyh5{F?^P2DD&|#;dwAhf$dd8kNh|-GBRaQ!_M{5d1O1+N004syeJBv6`OsYqTeh5S|S}!bBCODzs&SX6HP}A@8jysCe^4zw(9)OlG*9=QN|eM<lZ0OUsGQWgfk4MpRUJ=)T&y9D9wR)gp4rEyqj?W}Tj+1q*>xiL%V0vpG5l+^l!}^?SGI)82dV(f2FYz9b~O`udgLo2OUre0lGele9;VU|VjZ{U2>$E|!SqZk#UN0&_f8PhQkvKy}R367lqiktR~r^qJOgC#HLYu(-tPdc+~ssaDp7dGH7<-v-0<f}B#D&ZW9A*4u*Fkd{HWHV6;QWOau=>;plEx|+<zG->Jm%RhigV9uC+tS+5cdE;z%@#N5NpL}d_AEC!#;=X9d5nAD5!F4Ea265;w*mA*brkuXpEtg{5qA8bRgTqivyCC%SjFcC!){f0Ij}I=sM$^h@nd%u46Q-6iwG1%Ex+vwHSs{vTD}ZKg1#Jmi4z!A58WJ5bQ%KkpWn(kWcm!=yIgO<ExA)CRSUe%zgXL8Rj<%WXjHCzrHWPLIB5=GXOYBs65M2VQqN8og@pAP^4^j-?F)J&TBFc<%N4%g>e6%f95Ne3ir3EDFe(Cyy^Pe**TW@gX^#@m8XK>|*4X(WY;L7U_j_J(aK*lvZ9W?wZ6Z3p5O|RlF1XQS7L`h^EZ8{GqBHqy%K)XS5<4C%XxE<TQ8lDdtjS=3|i&wgfAA(NYB97-A`lS^IXNjqSI7#@miX9=+WT0Ys;14AZk7N&Oei&bv-n(^+zGrA+ROWSf@8q5_`sh8_<0A}fA}ef4p#kdk*U(0jF6cxSs)z;>iW=o9?eAeiQTOyMDCN`oWq0{*cj;I97aukeB*eFlPB`CIWlnY?A4Zjh2$XQ|RepsYC#YOEMoq``rRRH#KPc{yDBBUUQezduQ_<-5h8IU87ICRreZ;E=Es|b`3FA<^ibq`k2oP65R9EWgZ7^y?<}3JiyL`^O5uwwzK%OS{F`6R`F=H2$_}fP3ZWQUpVNK+QknXG3h@qtw#@gO~>%nJV_I`eqXJO}FwM!p8>>cGn6Q@qXPK<F<jf{yffCA~@l58lQFI1(0wnWWPLI00Jn5t=_O06VDf$A=iRCRad_Gi@d(3Iy#B-4!JtLX~}wWs5R!d1l-M1;se=hHoeyt87hBBDQaQ$aY}Y40~0^wrQ55Pc_Bjt=P|scaGQPVZkK3GQU?_1m<kjTU1YVL_rIeD)f#BF0-skfVba4gJ7D4}+?G+DIEbY*9Y}%`yl$@r-_pJ{nc?kdk%>LOSHdq#+NejMCjSQ6UaG<P9$&dJ^f@oQRtrcbC3|HevZ@cj*RiPm(^blJwcTeX+avPIu`IVl4?RJavc`IB63JBc87Cq~(#sj3|lZ_dbv;{&nxx8??x@+D{!4a!NyP607^~n@B!r)eN}8qc+a~7yu$afsnV%@80dx0+gN%)LAu60u@bR6U4Z|^6?~=fcSRhQvu7BL})9WA7aSK+cdRT)7X|Rb8rYw^{CoIo2NkNU9!%sNhQ%?J7BFxPSd3(Fcp@Nt7^i9kjwjsH@y(4U7a68n#CwxIs2D;zq}77B%|SsV1-^{V6;imtr8py&WRovx$^HwF-oOPNW%(23+DuODmc{YEqJHV_J3Z_sQp1@PRBIfCJCx~#(UALdL*j)cr-k&M*w}={GH45K5<&<K?qDF?@<@iv9719XI`NZcbC5DE?vaN9`}hAY|xPN8C1^(4Xlh|m{i3yq0g`C0bCO|2&jQivPwVabRfi*Fd%$}@ubT*0qyIxoKiGn8LG7R+H1XEzRac>7y*0&l%6y#`w6J9J@gG)6rV&`P%<t^*q1_@8ENJ-IjD!sh;SKXpwO$fJp$o3)udIBGJE83)7|Ay=<p5w_qj8d)V9QLQ11=sbGU$hGAB$B+Vq)VrA>wJwF1lx2|UfVm$i<ym(XNLbEs&fW+F@~b3o7*aCiBAKHw)<jrbSPqUGZ>h>KU0C_1+L@#p~(yVNc}PPv?Z@KUjIE7NpjRifkI#VV+~@^_!~jK0e%KDcUHbRDBc_XV}7=}^=iuJUX3@;47Iz0Y`jS;qUp*J>XzwX+_bQGTMG?^SU$_-T5^Yh=HZu-yonGxEf8PW~FRsx$}h@V}=75z>}8ub!Szv>)lbq<Gq%KxT`mR33wHK|2rB%sxFmF}f@4T%bc@9#!v+Pgl=hx_{yJ&~I;jsGf)J9Y6Na&h_}$l!gwQusa^M`@FUJ_eAK;#&r^2=pf^{yG(O(p}Ty6M|;{X;1@%?1Fs4Z1^YN1_rkgdnWV`*&?6lO$RWO~$|o8d){W|&X;_`eh!@31+{pIr>dBuTynd2(c#ei2^pmi_gikvK8h6Ow6*?b=nZO@9>>i<YYDOze`$sVH5&Rk>R>7NLnVp`1qJCXo{pqs@pMI&lp#vUHYU~qn-5#g%R4F_y_@KzyBcY^5@mU(Ly#4k4pFW}4rw5|@RW1(G{$G0FPyFhge53cbS60sa+<WI;1``gA9YNgzLMQa$+v%H{Z9;6y<6?TAZu=yeEBayq=cW4zWkpZ~a2qaSAaf!3QF<bF&FR7$+D{artt&AJNNN6?0MU%LiRkn1HErhj_k&}nR=+vZ`}C%eZDY%EX}4fCV#X$Da}e?*+BNL%i=32e$JS$sy4@8HX?M2;$nkb!z=_Xhg(>lqcmk(rbe~xX(RtR9Qh^7BZB|cw6jZvoaum9wuWVnL;*VqkSY1;3H};4huFw&g^4lTpM8D;wQ=Q8s0AnW*yBDU1lCX2PG6yv^+j1QHi703PaqG9G#Z0p+Pez%WJ!H+E7j3OP5J%g){f#`BV=-#ZgI4=$HR@9h|KkI1WGiNtaPflWCW>dpv^hwp)f1hFpPe21J}g8ys8BGQ!^Bl;t9zuP&IKrCm<N{^-4g~b<EyhYr8J*ZOEdY;yPwEps!gR$n^d#uPHJA3O>SOPnB=T@EUDSwYN0UkwzRu=b>;Y-?&8P5<R?{mLa_pK6#G@}4rsFyE`wPuf+b)#@wzED+?}*Nv<A0jHZq~PM(0{fGqrSRC0et-PMSBKbT_$z1R2vgC8}i!rtN}z$4gJT2LNc2c$Jp6-546nqaU@$B5L4e7kx$znjvi)78rn)H_!Jj5ZiR;-Y;kGe{hLV)zHqp2PUVsPfktl9iJqI{XfR`?Af_@hnko?Fgbo;aw2u=cS6S8wtL@yJ~z3~G#H!M=d?Iv8jO#R?bxw%pPJgad-CAe0o$Z=!uEnTV>>3*MCSycbWWtZ_U+!ib9(2#y{2~8&dI6gXdIJMyT<nJJ&^W({(j}w2{ur@$>$M@>6Hs-Nyr)6KCwrQH;8S;{s&3g*=i>-t#A0}M5n|I))U&(3eAqHw#V9J-pj;%?(hQ;D%3$s$qW}OsVX}C53uiC!%9|Sca7woQsF3}UD^_uc%zPrngMf!c!LdrC)u`hsrTyFgl5^icD1|ot+jU3IEnF5>zS8jkaoWbC*+!(Ro~_+azc5-0h=o4j?!$;jPjRQ#;9s-*hTKKU>!8(ZL2DtB7rC1xt|Xj2~3ij7)n;iivCxW$48Z>`gxXWr(Df3jDC5|0L?K5PC|ih&}VvRR8SxD0m$C(Qz3(s01tDMWliF~zBWuK8yMMwqW<yMKmFsoG%Fzbk(HQ&_1h4ctoe=3U1vN}AylMaq0M!Mtb?O$cx^8G9`>+ghGs;NwNQ9d<Ia^O_1Q~7G9SwFy6;T4fsoe>>-&_Mt1CD|14i~e(Q%MZyRay`nU329jJZ+@3xnbcoi~?NE0pfgk=KmZ4CrRsd-c+wq1+q-9#%n3ja69vygNg?o+$h2;~A$uDfBDdE%@?DPulmP#2o9<$=i_Q4BEE4s3SH8kle^;ZG)N>!~r)FREk9*Eg0B0s5;>f9KVWv-%G8jeS>;YCyYCMlGKa|AvH&AgUa!T?RzeD&levzi$#|2JXn0Q_vY!|wQpQLm<Rv=m>1sTw}dq2^J8(SYSR2eSkKLRj6eg`r1@>q9$=Fnal^o!Qs_0zpimyA1iea>9=50m6OgW)J=VK%YUSFud{E5y4(&_g9EFRDc)uWSD9hNuTZS>m2*?WBsW>ZTRE@R)bO%yubo2&EOBoRl7c*xnXVd$1TkC3ikT4GH1J%5DQx<o=$oozY(ssv0XZ>bfRzp2YAKWng^*;T4_0E?or*F6pJs=wULoo6)e#4KCraLn!JoD`F&?=o~DV$qT|JJof>hKaxxl~?u+<Umz_3!}&V@Z9+3+FV+-Qwx<VEIz-ecFK6c|g6BH+si^S~+%cNPH18@z+Yejz2;w@~<#H;=W;};M@(t^*>-Vz|b-loBACr98V{8k{e@akw}DyuorYyoH?+Zv^bs=#y$u}<kuTM6dP0&_z@Rrk~c{tiXcAKg4u>9Jn=kptt7Nv>V18wci~L$-Ah=O$tW(V=f$wSQ5_)sMgmX7I#FLY+fY`=G|SNV*>W!CQri3b1D_=0jjBqFC<$TQ+IY%TW;+++1^A&DjS)3F#M4h>xc&(t<_E9SN8efbc<I5J_lLI87jLJt*v8HvQ6bbg;;P|6175-LuG9R6)OFHOZRlz6dBii*9!x?-r=Tr*n$*$Cv}%pc1^9xw`WTX}X!d*G-deeNdT8<pQ{VkwWe%MGzo=<iJg6r3d$gBg-s76v7z$4eF-aJ#xSEW(T*L_)hI!L~By1Q1rOYz(!DVf4j!N0qV%n~JdMj67gLMB4Z$Tp9OFxsO9@eROTZXpP9TD(~-wIGxq0fV=nh=GS@r2a2bAomNPJaX?zI*^7(yi$sLPR`_t#02R%VB`1GOdYi^kSo~Q^Ql*s~#oVCP!9qQ^ajxW+u^us_?|RG$Q9=hO49%P*t0SQVdb_YOwW)a*srJdc@YDMx84$+Z+TEY^pmnq0<&SGwp}QZ@9|mSckNaU}b&{5*KUwV1eW#OjHke%@}C+wHimoCO8dY)B2*gC1RQ75@U{yG;J|1*h@Rh7-RX_HNfHoFaDYt7RBT$DrM7a+4LcPFPZhVPy-XJHNQ#)n_tEB$|EsI9Ye8Lmge4IbvC*h@0Dyk<=nB#)i;vV4~MWYQctP!C{2+155G>o#dNpBOX{>NtaB74q#BO6y~YbOp5Xg3%~*>|2$lP6Fk`E!dDF8m!nwt#R#nhY53lL4<!7&1i>mXQmi|cQ0Q9;?*qW+nJCupj;~rnc5Ut5|BsD5dXg2X_aEPG=z_(4uek~r|t!HU?Pbsm*Ht;l(8ttdmb<%Xv?Dc;6^8Sg}2^W>c#C~(-`#Zf?e}dKj&aLj!_iR(V#p;)&(NNQgxOZWx`H(!N#`&u}wms0SMmPkm7n2q{lQfA&LlFddESopB>BUa1k;r(;XrPmX$D6Q3nihE7=kGC7LjZP3RUCQof*R%%@|4=e@O|R7@x`qX<~XfBM!uIlK|f*R)SZ<t&J*h{AIt}buq}?8oFD9Z<+Y5d1bfaNYeEo*ed3%Vucm28ZAGnPqP8=vY-e0d%mI-LO^sTb$f>F&kuK515JTa?x#1{03M?*R(xsZfc{qW@gBiS{=ZWPAK?stTm9c~&i%LX)A|Lpd;prS65yy;9FyKUBgU62i3InGR32Y7EG&siNRqYF3N5C-^3^-=U23HZYIj<{#2%dv5ebl)Vs&)WZt;?_%hB-VoL@_(a;Nk^Zmlz<~=cG)0V~p|45=Lv%@iu&FQloc5*SxSn!CV>R!_}eA1z7f5OjGCC1E;AQ3%XT;8(8n1w|ZY)?JmBx`uWNGpB-bmas@p05{VnHp=+Wu=(@Y~Uhnz|7DuiS0e<kw2i?VsE}iTyUVZTD$@{-tXBdA2$9inZ5X^{{n{XT!Jkkvu+p4N#i&U6nrzf)=n4HtMINPFRs3B1U;J{4T<h@9kq@nA;AY%Wm1}+OwvIJM&%XCh45=?j$yb&NXHjG%n%scM^+b7gVU=o=zCcx}MNDGTkptl+6ddB>$VPG^&g?*owuLUnXFQN}VOiMus$XcbaoH5~4UO-wYX8}v;gT-4bZ+y;kdCp?&FS?8G(mE8mlWV;T*P+5Ium*PeH*Xpx?jwN{or7|Cmba?-aG;(Ujaj0J99&N*+bqmz)rwM#&|hQ%uw|6wKbi)n19c$TCsKpZGOb3^q7%A#69k>D3a2%r4OIDzJ&+sL(21iio!DZ%S?DyF4upBCieb{rd%&_7B0?1N899;$d`?buPEH7Tjarw8^~qh<pb(n(iTf~s6+wokD<d>Ac$`lIJEu2v=!M`=(H3Imf`mq$Ay)|WK0LJ#^PoxAD{WN^hY5K+Gm70XY6;SYj2^i<WX8>m1h$Os4l1*w4v{LQ_kVZ=K#9Mh&2j(J>noQ&W((2B-K94LUkk58{Ms{$T|cj9RE&n-JNBkS%Uqc^qib8#{mVbN#0`6ET*yfu4hON@O6aV?4rxyTb?`|CIZ~MEdIaL#zrV1xfXtj-B^cGS6pa}l3p3w2)paENqkS9)K{MFhP|yOjs*&A+C9GaR_c0%Wl407lG?o#22E+0oxj7))6NU*XWhA(8*cq*7U<R*yVZnE7rZoXhCLT@*^RdMN>vn9huw;ZdSnJAqly3&$YItjo5+hRc>(KN&GPsdH)bN(yj=ldoAXJ~|IRs7&`Y4H#Rc2xMO{Tsg^W>p7_SLqLPY1kaC8A7nFT51{1K!ar$z^hrE7s?)Le9-!bwvFr`>r_yk4`EKYx1hdz|O0p2q1~UmAhzKjk7981VFH0aanEo=P#fCPOY5%3)YGuutOoq<PeYc5&A;!^aZ@DLgL`&eVRHiBVgFLc{7q|sUF0tZM_bhN_sgsO0c|)1i7_iE$3;}-FXo_q*|#n8s1YbRloIsHrKD`t>{~Nde3%Ckwf!j=&VzvO%?tz@+8l#6u7i1gFAg-w*!}-EZn?Gn=1TMgo}a#+<p5G?A$Z9JMFxWAN$gM2l#n1wH5a7>WOcAU;i@n{MgjqoqKnrV+UZ+>Ab&}e$mfEJNNCKl%EIaXNqReQL~ksmsVamH8ei8^T5t=f-*kUIZ40vrBY)4{^xU(=`Q@39)A|f<=%yh1*`Q|*yhw;5=h!`TXYTBS(U`)jPzNvvucUd8Chf6b{YiC{^y47tg6mIUn2#pH&F?$#ZI;XKG?YfhrP{f0DV{0!F2|IQ0YGtc>wK(Bk?-la8S+o4aVZ|Dqi<X4id*~pmi<}{Gfw$0;0OEH^3yf9`<3Y=g+Hy{okbyZB;MTyq5v$rJ0xienT0{dBL;5X=H<lxN-mIxeX-*$u#T#z(Z<Xh>mx{nz6Z7`GViVA^KEl>YC{VBtChEZfTLp+M-ycF=RygiS+O1_ghn-VYI=#;+1OfgjLrN{>d3?QyqIx7)6bk)^v+wDeIlfEsm|!>WS3#$kO40PU`U!X+g*&9_E8{E63llv<VzA$df~l+8pFb!sNWJ@_22qr$cb+COGejzMxO-Xoe#W+ry}x;7^x|=scc}#y%hrl)gL*@_S-%P$=SrIQp;ugPbrnHT;k7M+U{Rad}@Ln=LDZv2o$rAT};`BiP_*@V%q*I=~V)tE+4vpol?^>dS-#a<QZTnqY+?q#jX(aiQqH7DVVAqy?k3UO9bZpd!qUrR<J{<t_;Y;|e<#E)HU+IBOkP%gB^h9ToW(R)&E}uzWbir#^&XW=~LMRa)~;ghcjqZdS1@EvYkwfm5d4LS1Yq5SyqmCDi5pPk%r(;qsSY%#6|XDh-0_d2Ot>h20$A;XP-2WEK!pWp{|<LE%(23XT%CA~OMITjjgL=z3=_!dXtX%y%*{b`N^quVR^I0J}2F<AK9Em+bb!`YZ>p)w~E?xh-^J)$m~`1}d0=ZdM*4lfVQ0_za`vDmASpO*J0qT8;4HpS=GC#!uIXWn*6w?skS&)~(EIeFatDph_`U`HcoFU{bp)XxBJau2qvzIa7|^arP?fN)aw6v2rv-)JiBs5IfdVGuF!5ky?`}{j5QMn>Wf@iNTb{J-7j0h1t|Vka~=pt%Y{jD17k6Qg@M<{gc^nEBRoz({~f<G$Z{#i+`%E8Eiulg7(Gl-RoRiC^XC3h48BgtAVhj@Pr@G%=jq~1>hY>&9YY8lg>Gki>p9ZcJ!tSJK@!3wt4=#x^yD@46fz~OTVqgXT4^P_(418f0`SxKS-Kv5Ix||6Od-7UDhya5;+c>9kZs5fz_(fZe?IG8y`$VECTKJeD6pxf5macRh&B0U3w#5462nw4&MlEV)YQcb>z3D#gTr;Gz?vb)Y54(&D2c13)&1OZ~>V3JU;V5@lEMe)PTO8fnFl7lz2N65Xu2#C?7D^GQY9(u(4)M297lcuy(9j-Jr2%mBq1^WvojWEBn1;YZ&L#ZC+)r;YG8Vt)5-hTigJytj18!uI^IGF0E{+H-*F;h-Yj1T(joUh7}7v{MX;TBzzYeW|zB5-*WyA`tcKcU;Wn$3VIUVidglQ+6U2;Q7z2RwourUzCza6nKIa>|LcX(T`ok^i?|UEaTw@iL$_(S#-rOAJ;_0VkFgvE#A>!-X{)jZwZ=X}({cz<XO1)24O2Ou?R}2(<a1nok~j}qJ#>VSS8my=(W%B+NLRl*59h`oZ%RyOb_^csmH8M>nGf;FT;C=0VGfxEFONQF%puobPMOfl19FfG-f~bp=XK)+Z@EH+<16Qs7yaa%3f8}0@AH$R;T<sNa&G`dOT!rDCg6MnUBZOlIZwYr@F&thlwhf}$ji0SZE;2C5@tJlLv&UqHnBzjRg)05g9tvnoCxN6@7=rI#hbmqy)t9~<G3MgXsv@xHERF@V-&mQ=w)?6eGsh3rw`?w%kt8bHefN$x+3<_hD*wMG*ObD{y-zjJ!U32+)hpCc09{Cg@}&vT4_LA(hAfBmlIWG&k<3uWM#~`B#;W)3@4o!9h<2&yvi&`O8B})V^ZCvtHSQD{PbOS@$`_1pkrRi;gf7Eox><0kj`b1LeFmzi<It7V&RU`EM|`QBMW%Y=Q!Zq@8J&Ik16yaACPrnhW~6blWiv}9oRj^L2omGEjBx<$su}KnQW%2mZ)lDA4mMOvx}^JfH*u_vP>pG=Qe!;T4X5`oPKSN1gBdkB|?9vCJ#d19Y@oj&U%zstcQGYL!z>D-$zHx_pJHmhK&Fe&jE?>i`IO37T4!~yd4VG*Z3Lq?OAsu?mFj#DK7Tl(eS$WjYAec8wvu`4$S(MxfVvmO(#j(je=0Z#hRW0*+zU|h%5lUE$f_Udp>=t3}K!l*Q9Z*>s5kjm&3-Z_1^x(?Yl2%ji_j1zhH0Yc2mnfv<9Lz;cM0*gB#X@K>=*03EYHu(b#5FjA1idt;N#gWGf~%BF5ZhA#5gq+=*awW!wI5=zL`6=A*|LJ2iUPxEV&Y{-CM;@dn&~@SHPH9(?M{15SN;ol{>Pc<Rf2r@p-A)RzaG`tsUSUmkes%YCQ5y!O<W2cP=#x~IOp_SBcxKlSDHPJMapsV@&W_2q}0`trb2Uw+7`FRwlI<$<TZJm}Py2c7!zfKy*y@6?xzr@lP!)R!N2>dTLP>dTKl_2oyO`tqYreR<%iFRy#*%a3#F%MU;G<wu<Q^21JjdElw%0gpGJu&$`hTgwV|2sNdv35RguFC<zvL8uBz4-r(W)G(d$tBIr}s>th{9Kp#QCapS`0fP4f%n+tAxM@`H;wNK^i~SIq;kssCSQ<!%pv(@ja_iFv$Ih)>K8MPoY1&=%;ai@8E<EA5h|%q#)@p64Iu)U9#Scit;r0>9GEu-LrO3%+C+!xTcAP#V66k&*&7Fk_4*_Y5yc(uyx?B4ZeHAK3jan8i9|6>&({bl6hhRPU?BfULZpzzzN%Ek%U;1lz`7`V1adP#W#nnsKRxcfAWJ#NB)W{`n_O;0)ahSjxX!F)BDL?SJE#zb4ohN>n(kzl@TFtmw+Gw=Y%(JmS89+ubU@L6~w;BX^69$A<g=}s#lxG7%fGpXJ7KR6GY-O4}-`g8^d#~S?CEhZ`={q+6UOm%nDw{QgM!x3{RQpV7Yc(ehVdo5L=k-^cY%CM&RdXT_QwwcFe*>FLL|#v7YwD5YLu!9}?LAW~>8wU4lGx<5lE{IzN6X}`%G}f>-Ia5`Yzuq5Y(4<rJzZIjE36EAsF>_mkxh0L^<}$?>_O|#ca<Hoq3Nb%GQ(aoVJ@Q*&BR*!V#>lOA=x9_TQ;nzn7^>rNZ`>bJFA!=tC-TT8qh4^Q|jyG%Sxw`Szu2aW5!Mtv%xHtxZzI&(q=*Ff9Kuq(g`lVA~}(U{x~WN#2PMLReSsj?HMtWr2Jq_A{FGWVz)CI&L6EWlWimR5pEOnqW#gteK_?9*TVP6YW>j!fVk?efVdZ0u|JA)&>nv-B%%PrO8Q4hqXgwwclmSnLHL$4Rpv&Pq0L)2tLdX8bJFnyp<w(n2q|{1wJK;ME$Fo(D(tT;Vn5S?&g*TT1MnWId+)rpa`xOnY=`=x-);KCp+m~#V;P;+Y@y8DW?AC`ryXzI)GQ3ZYF{esnq5rLA`Qeu$<8~CfvH-gnQN)U=Hk*(PT&&JTBI`EzO*gGRNcGt5i}2yQ36^#4gxeuO08vSbE*7Ho~)ETil`alh{V=p>w~-+F5k_dzZL|*ysf3$0Ed#$o1;RL*Hn6zy55abz0cot6P&`UrD%=fmP0$~v=MpmbDP-HrDs&0A}Dnl*s-HUrI0izZ=~%fa3h;S$kr2^+su0@BooS-nC~#dC?*)nveou~iyd^P=CBU$6MHz;)OE;4t_|0(y_z{siqaN}*kZ1YitC(MsMf3|%{>e`Oi3Kk2~k0vYXeK?tg9frvyI=ml7QJf@=d(?^3)p#xjC3@q*F9gS1xT*5!g6(xf|a6yRA=`#j$!se6SZdlNGx%#O(G^;<F`89s@E92}tIBgXKn;ang=AL@9F!0N3Z`11Y`^6gaZMvQq^&iIVjhkUXe;U*Z6W002BzyXZerN)OV`iL@X4a5o?Tqn4TE!z&xc0VXEl5n;x14~tT|^4;6Cd3Xr@I|#2s<C*71HgO~Zk_w3}>mFNj9Wf+#8ch9`J*|N~Wdu0O#($5EvqZUhsd;shMjU#hNY@&}BvNOq?L52|Bsh9_^VX+FN(LA6j$&Wgex{c3pAC~XaQykeWrPi+$%YA%8^rPUB`R@76u7+dfI-0zwx28Bpb8P!8L*nmOB+}mNuK#L2&@A4%t*NbHoNIgRG#I>fuvxeS$x;h9w(viv8A<a_F6YuVbp2;AAIrJ%3sbG(`+24Ze;O?rgft>D!#2)tAnG_tk;IIMAF2~3Jo?V^XW~0zp+7WCO&tIdoo)(9&kE~Ec`)EzA0|+oFBFTtN)AwWRM-yB9s3pPy-Guz{Q?Dwyq@b5J(&PPc1{Cf0G7IFiqS{gjJ2j2@_K8!BLhZ>@hA5jJLvGP<78az;MO<>ARKhmU_P~)0ctB6%$Ek#}>f4#}*lyEFS!%-^CgaKEe||5F}W8Bs@$w06<A5C6;}#-k!2D0WsWdgp3S}<ic*vBM@D@76b%-E{POioaPz4$M9K|1>wL#8x{!%BE|@Hf~P%yD6x!SJ>n&W2EUz;Vz?msj0oe+CH%UG56o|K@7ngBzwgLKBO)A05#Gm)fWeT&t|sX?Aj}iQ48${|&8AI@IAX*nc`8{6ik5?=CzGC$8S|wRm?t(f-4dhD{lC7$(2aa@{jYrBW+4|u5U?bWp=~VH!;-a^K3V)oHmFUdr~g0&A#9>G_JSB;%-f_5)J&QRT1qS;((SkE@ocG>e|Xq9n+V(u{XP-`eMEwgfNLXUv#vGt5iD<MO}^q`@ioYy8E=XVjt&hNK7k%Ui4;{TBsU(mo-7uUakt3eAkYY5NY>s;h?7SZ(4hMA9}j14Fc~z*OCtkW>)Z`l)Kc4gUDq{4m(~#~O$7AQ@4Jidi8M)A^ug<dPS1$Pn+TVPI(Xwpi7Q(<d)4$q2Ql;ZFx?o0dcbQmvNa@x&KZwK7=hZ5GEY676I3iHWKX}9K=Nr4HT6x1OC#_&z5tjR0VTYetl`MO9(8pj4Am?r{lRipkj%?Q?c1QT1H6z$KsHgo0YYnuI0ah$1Sr#Q01{MY5uE2bKid$pX|tBI&}lo+vIPGIo>@~fs)h%4JFH7+bGwm5zKK@hK(ZZS&^f17zP1@$1QtB)2x?elUfemEK|}?@wNW7z8S=9eHcl{kEL6WDO9=YM@c7_fk`X$A>larqyuNb!2FIOTeQ@ln`#*ki{}aN=S4}RnrT2QrUt2l-l?^F@wDd=_WNq<L<YjILBz1uivL`%}9M@0LetBjD(+#_Ij1$a9JTbYj5%^&RcZOb++a;H&lO)^p<7JSsoe-U1l4Y0D{h5%@Qkf&<=fDIl4~7+B12{>wEkrv&M=4-(yRh;@fYpkyGy)*pyxXNr@XOQ(CL|f`lAS~nsn<H!Sip4+m9d+y8=-<<W!bp78L#%mEOR#w`$u&4-x1MLv6`ab`3Yq0=p>+{5H_e>-dZjSC|io>ITAHg1-1Ykj)pXCyv$5QBVmtnRR#bXm{w@nkR2aD-T?X;nPm+DjrRfTucC}gGTINX0MAG<a<m1OCs*jm!U`~7^jyB>kaA5)AFQ<_^W+8|GdBLvS|s2wHamgL4>`b$K(nEscF9h2$eJ?v*wViZqQJDAxdM#N<ZF_6Ls(rRxe%a9)Dd+Jy2-dE=?+T^jBOpu(W}ANM#}_g5N^HfRbJCxoP@$3bv`PWOXbdozb|p_u{NhYg;e0TGzWrW!M*$j0a3EdXoIySJNay`!s=HD^}}cM-KQY}7&s0)Y;dM5>VKb3O27W7Br*51jxwxYo3!RDfv=0|rBeSbIkfC<z&=i^0|rdgG@WBvQAZV3GBy%5P#q;J**_jw{s`?Z5yd45=A3v$_i5y?nA_>IN85f}nWZVuZ4A7&YPk9D&=754gimbw@3wCFgE_ym`iLCPjjbd$%}szWHbklKei-=vc_c*E{8lg+EFam8aiS6QnP<GF4aT0~rQ-E69>57ay&gPagEv+=XgJHT9VMAtc`3i41};Hf1aRv@!?E4ixl9-%amL4)M#LYTq)^Qfu2!VU%v^)#5zC(?@#f^|8%LW7a*ryniIl<!`@F#i_!SB1%mf{q<o~z;rjrWDkaYlB&Z#VUZ}A6Obx8y+dFH#zZ{+$wKF%;=RAIz$6mwX_h}eiNTg$&2;Q*g@+j3*jvdxK$(hLXuvi_dF9p(vYG@Hy2BAd)3ON@CVDyR=FY^JAHl^8K_b9WiRB!~-01yHirq9GDR!1=D4u>cH43V<<po)JghVmM&GCi9q;%$^dtA8sIRu>MmrqU^pj=dDt9#|W#DI~QQ|$~BjENLc26EvCu&3ep^RE`)O^V0VU6F@ZWUTdQB4C0<*68$|6)oSE=d>nK4p<022hAnonM-l@T%;&Vs@V)Q~BA--Xq0Pz?7`UYO>Eu)ZqdGRHVcche>ti_e}qr{!;Awmfs5g87I5n0H68rZ(@@I1eWKrZGO*-(fHZ~6$kuy6~i+cm-AdHxZByCw(81~($SsR5aX>}q-ipSyA4GTo085KiQts*;*+jaolQNn7$bA>nRL6JFmziA~lC1}EA3!6$FS+tNvPf{nz+!92gA%~lxLABFqLQVG3T`St^(75o36Q*52IeFGBq^=0al$3jv?DH@!aZ;kJ(c)7x(HRaTHY3`dkZj*ba^oxEV>@+Kz%zx%tK-1OppWVN*IP}{mUs$IHB*mr&>&@WQ`03ha*7pDpuIjV*>#M8Z5ZtrxD_2{ca)IkD!39OP2rhEHAGpBu1jlhMSkIqf=(kh1)P66Cs5A4+3-h1p+G_cA@7A%EkC%FjXIHL$IrQ6^9}!7?G{uh{eh3KkYixer_xRTYG7W~fNfA%ev4>&Ouik5fE6)v0Xyh`0G8|%LXn!DCv!s_wcXxi|+riS_i8mg6d|_y}*QzIQNZwiXgQkc3(daqlVvQ7&9#V;|UOKjV<@2HEIHYGh4jblzhFK5M)>+9|tHr!WvA}IHh19+E&IMwX>v<{1$(a1Tbdsf59Lll|U%+*8Zht87+X$)8pMmOT8otxyc|-w($o0|63&CY9y>b83ALLRPDV9sm>M&)n^V7x&FPu{cW{KTR$N9Rp5Q*SCSoDbL3L<3GNe^(ztdAm7GTXV-WQQU@+!(Qo7R=R+jS~q+s3lEW0Iv~q)@Y8umzx=JS1MtlZ%G<m`Se#iltXHxdO?j7YN376%12V+#4cQG%JPtUbIX-f;x%zOKq6r&J2blS1qfJ>iZzV%?w}6QU|vuwXRaY*BlH?P9PCPZm-j6Ky*(t><{e6<ZQkr^crv1LKcIEThP4&kd;!I~iPj{1b5L90@C!(5g^iqp-%V0fjKuM@HF#qqrLl8P*sbVi$a9#npPiK(f1aR>k3XNy(`-OP^pV65GOc;CGghcGRfH5Ge#@6Dj?7!gpD))Lj&9^T1R;XD(?)|MEI<S8ojNJM3293nV>5-5N7`U5XnX-3l6J&7p*cBpDpfw_Qlw_&gpkbCa9czj?*8+UOieXR5^4@RY7hxVm6l(0_!=hNbXuMm-Ho3#(9w+x$sG0Brh!tYk|$bj5P;6(%$pC+oEX|iwI&?_39yYSaxM^wXN6%~n@Ag*77+ds=~x>|16n!`WYu|UKtJ7=%;Qz)b%H3u(1`WmmrW9cAgs3F=JI2$*246;nSYi~cb6{nr4n)`Fv9NQsi7TN4i;GQa{ouzqCz}s6H_bRUMMlqw5)1P_j=qSa&Od#3US-LcTSoceb;tj!?WFv+Qq1B=`o?=JQ6#*@RtGhg;k@!agf<YDu2AtVo{4cX%S{{4JYsg*qyIfD5m$X4mlYwW@!wHR*OV3)e4|kZ?z;v)v#Pz*Z@;WpEmF7!^B(dPk0wO5NKZLC75r3bLYVlD`azR!=ix3^wu`%z<EnFel2*}(pykMaf(tlqP2*ipetnWcRL~xQ%2XhOs^0F+qsz77to87=Hs9aXM9oI*Ys?I*mw;s5M&A(Rh=W)aRigXYn%=K>=oSB@Z%@Q@Wo`Mck-kAZ~n#R1$kdY3d8f6{2eAIPM)qyxO|(ur<&*E5+>bNK+-lKNS<gSA#hgU&D4<?v_Z#!)0GucT)ox1{?@(Quk{DjZ}$-wWKvj?lspy^iJ1><k;sc^WDgw#zwNk_1I8_B#PZvO7i&K|*2v^lO8I!5XToz8S=Re=ZrMTXZ1VU+jr*fx7*XkETp~ogYf?2=$>fs+!GdRKipLR2E_~C(hPuuBJXaG$HCyagBK3GVING^P6ED3YQqLqNfEg7=(JR+rTKU^u{QJ$~%6Ch^3!K%Zf8YgQT4w*G#O42_q{skDnacr6iOT|t?R{My@az(i*h&K4af$Fe(`f#Ez|dq<!L*ovAF_m4o($n-NH6q3dclSCf&)o@zfgc=N%+vdS`Dn4$5(z-5hO<<8-62?JfhK1(Yc(CB~i*+?$d&2ao1mdN1#=8m=ZT{MqsZ6%(7)zue11QJI!(w$i06<B<sQCI4#NNB3$xjsL8Yz(vekdL(WsqWJ~A{-nAsSU4(1k7++ITNIzs!?wJr@++cz*-0Zp|qTq@@H0Vo6wBH2tN|IKfM4p`f)I`$ET!%#Xtq*qsbS)j@8&je+X^M0x)}Fo$MfZOB_5KH!NIJFIibUP{EAOih*{>}>s6+pK?(J_?!MV`f60e3c#VBsY<#u^0k$$!DI;{(-Mf!EcgWqv-jr3`S2eo&Uz4IpN$a<~%)xTLzDyKbIK7@5EU8~8ZHCxq7M>fB#{{E9f2z9Z%{PIhLLp;Cna%x`Ux?s&adGXp;YJ5>nFrc6KVJ~54sKJAi^8S|&`{7*VHTzz1O8Z~vT|d`*<7Z^cabIvs^B0EpOpZT0wimgc>{TFJl}R|CDZ&2nfd@AP)zWp3&sh)>{iqlZuFQ=6+p!N!rqc@Xvwl@Sk($dxwlat+;rPf0GhqM)DzLdO7#yLXe<f};a*UV_AI<?Dk;(j;5rGzm#L^W&iR%Gj4;~nS@-y=#h7%wGroD(HhoOix14K;)NtQn&|2i6wO<qa_Pt9t$CxGrbmzD^yg~Sd<1yGCTmT9V~!&?2XHf!k|4~RX2N@;e%2`vraAZzLOUl7BBn_Hky`MA6Ic6W&yy=n7yyv3I4to$52DUU6(!u%~!q%iIK1{qJYJb2r@NRL8;*f1gHk}3d<Ys`${Rzm8WH0fbCFJtXtL)1`Y#<>NvBv%jE^aDVu&~<JVB+D#!Wt}^l87h@DnE`dy--Wrr%!2{R)G7nH=5}Wnpr^7-wgQZk9*B8{m9ch&p)onHxdWP^fgP<k<y<th<Ajj3s&j-bqkKjewq~z$N~J+2X#(kiHb`bZ-Y!l;A00~4mQva~cl-W@w~>&6ufw4oGT;hnuxw{f(AlOvBf3ztRZic4toh}KY(tU#aEjBdp2o(2V$<~~SZ5y;b7WxTagaF^(condz&8QBpg0pe?y4I%6t+}|O$km%fRlL<<f|Rve$*`IMz-96K!RV9v3ZCq3TJyLfuYHj-H)}_V%8LshqMH!QtEmRJl+y75FmIOWi}5~<m+C_ZwP;!g~bAz6f#Ti857CCRoxvN=H!v)q8k&lqS*AIhF_ZZ8i{^+WUKi533hi6wZ-Qp=MEU>2Amo1#WheCXgwKBeu_PV*-L$w#yGd@%&<Ar1tsbX7ZRUxM(m~Rk|1|9HP6RR&4ADnhw%S{u7=?h4z6brJe^#2WwlFJxT3}x5kT+<ItMk!>-jkyc<&D(<9olnExxn{q}+tYSf1AQ)~D>P@NtgWNq_-nKQ(w^r~P`%uhHRY6<ukw5v#p4W+==|xp6SS@<xZ*;7v>5#MPCG831)d&$F!G56<BkrDafb+%5H|2xLg`94kUX_Hvh*w9NxUs2v|(xS8~M)*?amJl~R#L#6djVqfltOIk?U8>2;#uvW)<@RrhN;n(M69V`rt%fW$$vchhpA2tO2Jj@wI>BJhEe5IIz@puMKR@kOerGJl8%ibxGN6&H8L(y}0={;fl2QRrK)AMEmLZ(}OPm-n`_}_2Pz?<Gtmd4o~$CyK~*zv57jNwR~IxC^)J_mT@uI!P$tkD|)ww=Idq=ndR&N`nt--BH<J_BB4UF?Gf{Iv!^3FvsY5LO<}I|K9;lMhZ#PiWr9N;{(>@(edWF)#MPq{Ys^68VY~4zaDVB^BKP7epl|U!dZHJz#Je_l6}J_ZV2edtUl#=WYwm_=LwR2zMs#@W<G%m)tvR-V%7LKfanTJbMb!!b@n&MPBDzC6F!t>KR)6S9;%FfTD*jQ?!+OU;My0<1IwP;EpcKvE{dru!<8*sjfza#MHwt9eKI);Y&wfh9~n@tE}CzdE<^Ubag~&stN7wqgX7CjOB%QvhfZCpbdm}kY96BN_S^Lvj&K7v-b7_F&S<Jh`j-YkuXD%I~+iNIm=OgYfTZ5+M3_lVnCV82b#=*Pk81+6kcQ^y_{Ai?oT@3KRN-W{nmnRwA^gFP=s-+PFe{kS1=Yi2Owmb)}Eb=%t~dMtBKt@_Ga(+*K0D@uQ}Kbx2z?8rh>aN>Rz13#2Bw5uMy84<=_*}Yl@nRHO5+>lkD|sz;P13%Zx|tKAk1&^N7$T$nM1K7o&xpZZHhB^)ZmZgh@E8trkd<(~m$f5{KGbv?T&;(hY`@VI`f*5;5buJotv}4hducByepLJK8Xi=xqMT4gk=!X?EZxU{G4pLlzGMZ<D&#xCt)SO_kl%ShAN$BF`aif9SpXUGJBl3s)S{Q9ZVpUws9?!Nto)ahPA}c+nil9qb|Gv70o_O`S+aRSkRU-_=VVHi!D(|E|J6dB}NAf66EidDoRpgtYN5$wljc(}Wc~hpJG`1#P}z{(k@*JQ!|idq}FWf=3Yz!CoN=i|OO_W9&_yn$OdfRrBQX1z#gN-!ez=HhN6>mUR>Myg%z%DRsP#JYuZfUGR8449=LAvv{RUJ^2=HRRX%trD(zgkM2b52WzvhISk(*e6WA^Xv8k2IQ%5+5G&ed<6lEmAenSl_|Si2mz`G78hz1gs+afzzNCq&4X`C<Xaa9!4`wQMT87^U05c|`U@6_!2uK(Tq<a$w-`6YO3m7PIT`Kl#(G2xJpw}@YAPAFBJIOTXUMm&3$He(=z4m)e$B6eS_AF@WVf|V$g(w#{mR_;R+^HVWW6~V>t-xFB^=G9HBZf3M&#81cXYS6}NW#S6PUjlB*<`F2!F`Gc(7(LqM%n?LbC)<I+Z$eMPRq@Uj<}NFsk?kf^hL$3{cq~QXP*o5l<OLM$1W7QC#1<Y4I2!(W(;x&M4M&#-ZhydAEBJE7t6Am=AnwKlA3&|!h%!1F#64Om6bdT>Hy7Eb}?;9jXkFN%8J2`;9FE)@imDK+{e*s1et|D6N1+$u?lzO+VMV0nU%@Nu1K6+r`sAGsMjj-{Qgh%T5EC;&x`!2Lu|xBxAgWYy%2r;KTvv|y(-yLAAxVjLqBGGEBD*>DM{Gn4ZGTib^oR|mo{x8<`G6)+)wKUV*z2y{j;V1YjZ1M=bEhMx)34pARU%_|FeZ&8hGPwg@^tyn1$G8BJ>VCt3xrv^Ubzc2Nbd3ZE#!mN@qk*fk!LeF<nY`0TAzs0ayO6Kh8PiUhRv@%1L@@z%{|psoXlb`r}O`GaU$4<S>cIDzbWS^)7tZT{^`?-HKRy_&T)5+W_TFgj&aO+h~;qYY7PviwEuNSrW9V+|h|UVLnhTKxXROB`<Ocob`KqF3RHx0;0O-bK3|r?}+a4p*z(eXkq_`fwN!iJ+y~|^c>q9Jh}Eo1x^GXYge00nnRQA27asgZsLC6yRmLJxCSO-4GXk1*(W6&*Jm@RN1}VpijXZQ32Aq=;HVT8GT=Y~INQ0<h+BU2kbaBNDA<jRl$v_hYTVsmA|S2ZaO2Y9VR|bgmG1t#dheHySHC)46xRvQyuZ$lEN>EGm@5#LUJ>Oy5x?FWgpw}0VM~Lt)uc6EW?WjX!Gfera}cwh$L3tHk|Jb-O3=iexnNi~l{Ryz47JK+NyM)VxF@sbhX~TQiEfQ4)GPMeOw3jF1#yzMt=pTq%oN^HJ}0rG?K+3RT1k|fnM{koiT1$`z`M_Y^@?DP)G4ri0~0BBGka<QU__LMb}4T%BVw}In#pNc0G(v_uOc7aOb}K<Q5pX8VtA$fSm3S-J@KBxI?Q3~mI|P;{}vLM1hDCq&6EQA&aU%(yDRG&*<ibtZ*tU)!f7qOWm2kKMcm7cQ`k4itzyJhr}K;(>%EGb4OcIJ^Wai`4=5NiBL+X(S`_-x9KxSoLfFj984LF0S|04lhggiJh{3G~;_oiDBZNO$n2%<@*0Uf@fg1VjwBdxLA}~3F{U`=(U6T^Q2F<J%BUCvosyOg<xv<AEG1Ya=BP8WHv+)S->yhRr0fc>$2e>X?@16Ya!N<4PsvljZ3rOm5Oi$Y|*UeGB3on%1pPAeW_W&B2Upp#piN-KtY>k;>7d~0+5raGuoEy|f`g$Tgur<x&s%w~t+li3Dz?vE}B{iJe8rfZKA(C)Zb0B)F3<8^n2pf10z>v+5si=|3D9FaqIWbQk#Of@cv*trXO{~#8e%5?r5(X^ROXoJmDF3V~v|rh+ZcNrpf(g#=qf92#t!i5ck9dviEIW5=mW$4`)P7T07bDk@c>6TlpRQ-wPaPw~1y)7h<%><vFr&RJ7w6so^7iVLlNtA1&{(fAJ@zm4bFCSBOIE=aMa*$#3;}*138L=gh~Y>{CJ?6mVIpSmQC!bPg~tke!uHv`HmSWMeFm(mj`DlC7^`GMkv<`zk|gFu#-<eYTe1Y9c&()2g|q`qCw<nfD8JSV2&T{n;v&%n0yeq1KhV0x*u@jS-Vgy2(ow(33(mC8<zTx1ldS2h$`OasFY``=?O=xVJ?Ysf4C(c`mV3Qe!A_PhrPow>;=7Wx0VeWi>>lkmn=O!>Jw|{V@Y&0aXtvk>$lS&2#M#RgX2n!B-#Vknh?;9*>n?w5Gz##AzPqleZSms$Pj9VUAE1#ZlFC=8Nwy<8?4vVB1&c{A|4T<+R!5YzOAI!|%t)J=qecm1ynW4uRN3{>1FbTB9jrCd3<j>V3$2ct%cRz`*bMH#G2pD}z}RqX>PKy^rCQIL)7QaZ<IXx?5!$P^be!EqJjl+|*T*BxKK<R9j1dS!o${)KO+fc<(Z={0`^P2+a61)ltKT|Q=x3mTsCZe}rOfmTQ_-<kA8jo%6IG>!WA`>(M0=FJkj2cGk@rUrM<XM+N)H*wXmws*&tW}(%M%~+wJ#2KXfJj*s4u9M2!Hu*OZGrV7i!Q8I;@d=!A`yTOYEXPtXqA<a;Hd~<T3Z=9oI8fGywUVxScc}csps{CvwhUl&(L!@n3iEE_EQ}uljnylXr7RcjMTeUu-(?O(eP*$(`S=&->u}PTd|mmnvGi95a6L-ny5eT95hs{R4!jhxJHbghcUr)Q5P~JJbGP`BLxw#X`tLWI}~#?b=>E`*J!yAXtdDq+7o>TqvuZ=nEE7S&bVtlodWCY6yFR8x3uOH-KDC%0KN@r2Jqn9yJeg$tXYAYehG~*k8Oww0LQ7+J7Bz+IQ7&+IN3%+IJ~$YA)Ng&qJB>a%x?Y(@bbit+1OKmtZ3}axATN;54zcB4U|`Of2GO*HJE&S94*63o@aBqiOdBnJnl8)7lR5U|P2u8&6v;^hKq+pa?8>NTrUHf^>C52jJEs(qrtm)$qTmg3N7HAFW_v0WL_KB^>HDYkMtbSc31%Kx@E$zEKS>F8w{^3XUm9+wVxGfvf(P1X|+bqSt`3It^=5EsCLmqw$}H`X-h<9eqGtMMj_Pl+OyxPL6_qf}LAJ4tARh+O;(^XtWlkLDJ=5WqzOKl+_AG8?pR$cj-1xABmga3hMZV{a@H`*&0;c5!h6tB5@if?th@upN_R|n+!_<^n;$`%||Erf2%Ejcuc>k2$}Xamzi(K+>>Yn5o25Ng^I2PD}GZP9)(cH!ERG7U~!-d{kFdz#K-laa-nW#&M><{bq(0ZbE9%0P9sH{c5db!IM~PbsmdT{-c>8dzUDJ-RHUw7m4R>l>K^7)1ukA73!nCA53BzR@xQB%')).decode('utf-8')


def _gear_build_catalog() -> dict[str, dict[str, str]]:
    result = {code: {} for code in SUPPORTED_LANGUAGES[2:]}
    for row in _GEAR_TRANSLATION_ROWS.splitlines():
        source, *values = row.rsplit("|", 5)
        if len(values) != 5 or not source:
            raise ValueError("Invalid Gear translation row")
        for code, value in zip(SUPPORTED_LANGUAGES[2:], values, strict=True):
            result[code][source] = value
    return result


TRANSLATION_CATALOG = _gear_build_catalog()
del _GEAR_TRANSLATION_ROWS


def translate_message(text: str, language: str) -> str:
    """Localize known host messages, preserving captured paths and filenames verbatim."""
    catalog = TRANSLATION_CATALOG.get(normalize_language(language), {})
    if text in catalog:
        return catalog[text]
    for source, target in catalog.items():
        pieces = re.split(r"(\{[a-z][a-z0-9_]*\})", source)
        names = [piece for piece in pieces if re.fullmatch(r"\{[a-z][a-z0-9_]*\}", piece)]
        if not names:
            continue
        pattern = "".join("(.+?)" if piece in names else re.escape(piece) for piece in pieces)
        match = re.fullmatch(pattern, text)
        if match:
            for name, value in zip(names, match.groups(), strict=True):
                target = target.replace(name, value)
            return target
    return text

# ===========================================================================
# MODULE: gear_studio.schema
# ===========================================================================

"""Unified parameter schema and validation for Orca Gear Studio."""

pass  # [bundled] hoisted __future__ import

import copy
import math
from typing import Any

SCHEMA_VERSION: int = 1

VALID_GEAR_TYPES: tuple[str, ...] = ("spur", "helical", "herringbone")
VALID_HELIX_HANDS: tuple[str, ...] = ("right", "left")
VALID_BORE_TYPES: tuple[str, ...] = ("none", "round", "d_shaft", "double_d", "hex", "keyway")
VALID_RECESS_SIDES: tuple[str, ...] = ("top", "bottom", "both")
VALID_LIGHTENING_MODES: tuple[str, ...] = ("solid", "web_recess", "lightening_holes")
VALID_SIM_DIRECTIONS: tuple[str, ...] = ("cw", "ccw")
VALID_EXPORT_TARGETS: tuple[str, ...] = (
    "pair_separated",
    "pinion_only",
    "gear_only",
    "fit_test_kit",
    "full_suite",
)

DEFAULT_PARAMS: dict[str, Any] = {
    "schema_version": SCHEMA_VERSION,
    "name": "Par Engrenagens",
    "gear_type": "spur",
    "module_mm": 2.0,
    "pressure_angle_deg": 20.0,
    "helix_angle_deg": 30.0,
    "helix_hand": "right",
    "face_width_mm": 12.0,
    "addendum_coeff": 1.00,
    "clearance_coeff": 0.25,
    "root_fillet_coeff": 0.30,
    "tip_chamfer_coeff": 0.06,
    "auto_profile_shift": True,
    "profile_shift_g1": 0.0,
    "profile_shift_g2": 0.0,
    "backlash_mm": 0.15,
    "xy_compensation_mm": 0.02,
    "elephant_foot_chamfer_mm": 0.40,
    "center_distance_offset_mm": 0.0,
    "input_torque_nm": 1.0,
    "pinion": {
        "teeth": 16,
        "bore_type": "d_shaft",
        "bore_diameter_mm": 5.0,
        "bore_clearance_mm": 0.12,
        "d_flat_depth_mm": 0.50,
        "keyway_width_mm": 2.0,
        "keyway_depth_mm": 1.0,
        "hub_enabled": False,
        "hub_diameter_mm": 14.0,
        "hub_height_mm": 5.0,
        "recess_enabled": False,
        "recess_side": "top",
        "recess_diameter_mm": 16.0,
        "recess_depth_mm": 4.0,
        "lightening_mode": "solid",
        "web_thickness_mm": 4.0,
        "lightening_hole_count": 6,
        "lightening_hole_diameter_mm": 5.0,
    },
    "gear": {
        "teeth": 32,
        "bore_type": "round",
        "bore_diameter_mm": 8.0,
        "bore_clearance_mm": 0.12,
        "d_flat_depth_mm": 0.60,
        "keyway_width_mm": 3.0,
        "keyway_depth_mm": 1.4,
        "hub_enabled": False,
        "hub_diameter_mm": 20.0,
        "hub_height_mm": 5.0,
        "recess_enabled": False,
        "recess_side": "top",
        "recess_diameter_mm": 22.0,
        "recess_depth_mm": 3.5,
        "lightening_mode": "lightening_holes",
        "web_thickness_mm": 4.0,
        "lightening_hole_count": 6,
        "lightening_hole_diameter_mm": 8.0,
    },
    "sim_rpm": 1.0,
    "sim_direction": "cw",
    "export_target": "pair_separated",
    "auto_configure_slicer": True,
}


def _to_float(val: Any, default: float, lo: float, hi: float) -> float:
    if isinstance(val, bool):
        return default
    try:
        f = float(val)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(f):
        return default
    return max(lo, min(hi, f))


def _to_int(val: Any, default: int, lo: int, hi: int) -> int:
    if isinstance(val, bool):
        return default
    try:
        f = float(val)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(f):
        return default
    i = int(round(f))
    return max(lo, min(hi, i))


def _to_bool(val: Any, default: bool) -> bool:
    if isinstance(val, bool):
        return val
    if isinstance(val, (int, float)):
        if math.isfinite(val):
            return bool(val)
        return default
    if isinstance(val, str):
        s = val.strip().lower()
        if s in ("true", "1", "yes", "on"):
            return True
        if s in ("false", "0", "no", "off", ""):
            return False
    return default


def _to_choice(val: Any, default: str, valid: tuple[str, ...]) -> str:
    if isinstance(val, str):
        s = val.strip().lower()
        if s in valid:
            return s
    return default


def normalize_gear_body(
    raw_body: dict[str, Any] | None,
    default_teeth: int = 16,
    default_bore_type: str = "round",
    default_bore_mm: float = 8.0,
    *,
    defaults_template: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Normalize and clamp a single gear body sub-dictionary (pinion or gear)."""
    if isinstance(defaults_template, dict):
        base = copy.deepcopy(defaults_template)
    else:
        safe_bore_type = default_bore_type if default_bore_type in VALID_BORE_TYPES else "round"
        base = {
            "teeth": int(default_teeth),
            "bore_type": safe_bore_type,
            "bore_diameter_mm": float(default_bore_mm),
            "bore_clearance_mm": 0.12,
            "d_flat_depth_mm": 0.50,
            "keyway_width_mm": 2.0,
            "keyway_depth_mm": 1.0,
            "hub_enabled": False,
            "hub_diameter_mm": max(14.0, float(default_bore_mm) + 8.0),
            "hub_height_mm": 5.0,
            "recess_enabled": False,
            "recess_side": "top",
            "recess_diameter_mm": max(16.0, float(default_bore_mm) + 10.0),
            "recess_depth_mm": 4.0,
            "lightening_mode": "solid",
            "web_thickness_mm": 4.0,
            "lightening_hole_count": 6,
            "lightening_hole_diameter_mm": 5.0,
        }

    src = raw_body if isinstance(raw_body, dict) else {}

    return {
        "teeth": _to_int(src.get("teeth", base["teeth"]), int(base["teeth"]), 6, 240),
        "bore_type": _to_choice(
            src.get("bore_type", base["bore_type"]),
            str(base["bore_type"]),
            VALID_BORE_TYPES,
        ),
        "bore_diameter_mm": _to_float(
            src.get("bore_diameter_mm", base["bore_diameter_mm"]),
            float(base["bore_diameter_mm"]),
            1.0,
            160.0,
        ),
        "bore_clearance_mm": _to_float(
            src.get("bore_clearance_mm", base["bore_clearance_mm"]),
            float(base["bore_clearance_mm"]),
            -0.25,
            1.50,
        ),
        "d_flat_depth_mm": _to_float(
            src.get("d_flat_depth_mm", base["d_flat_depth_mm"]),
            float(base["d_flat_depth_mm"]),
            0.05,
            25.0,
        ),
        "keyway_width_mm": _to_float(
            src.get("keyway_width_mm", base["keyway_width_mm"]),
            float(base["keyway_width_mm"]),
            0.50,
            40.0,
        ),
        "keyway_depth_mm": _to_float(
            src.get("keyway_depth_mm", base["keyway_depth_mm"]),
            float(base["keyway_depth_mm"]),
            0.25,
            25.0,
        ),
        "hub_enabled": _to_bool(src.get("hub_enabled", base["hub_enabled"]), bool(base["hub_enabled"])),
        "hub_diameter_mm": _to_float(
            src.get("hub_diameter_mm", base["hub_diameter_mm"]),
            float(base["hub_diameter_mm"]),
            3.0,
            300.0,
        ),
        "hub_height_mm": _to_float(
            src.get("hub_height_mm", base["hub_height_mm"]),
            float(base["hub_height_mm"]),
            0.5,
            80.0,
        ),
        "recess_enabled": _to_bool(
            src.get("recess_enabled", base["recess_enabled"]),
            bool(base["recess_enabled"]),
        ),
        "recess_side": _to_choice(
            src.get("recess_side", base["recess_side"]),
            str(base["recess_side"]),
            VALID_RECESS_SIDES,
        ),
        "recess_diameter_mm": _to_float(
            src.get("recess_diameter_mm", base["recess_diameter_mm"]),
            float(base["recess_diameter_mm"]),
            3.0,
            300.0,
        ),
        "recess_depth_mm": _to_float(
            src.get("recess_depth_mm", base["recess_depth_mm"]),
            float(base["recess_depth_mm"]),
            0.5,
            60.0,
        ),
        "lightening_mode": _to_choice(
            src.get("lightening_mode", base["lightening_mode"]),
            str(base["lightening_mode"]),
            VALID_LIGHTENING_MODES,
        ),
        "web_thickness_mm": _to_float(
            src.get("web_thickness_mm", base["web_thickness_mm"]),
            float(base["web_thickness_mm"]),
            1.2,
            80.0,
        ),
        "lightening_hole_count": _to_int(
            src.get("lightening_hole_count", base["lightening_hole_count"]),
            int(base["lightening_hole_count"]),
            3,
            18,
        ),
        "lightening_hole_diameter_mm": _to_float(
            src.get("lightening_hole_diameter_mm", base["lightening_hole_diameter_mm"]),
            float(base["lightening_hole_diameter_mm"]),
            1.5,
            100.0,
        ),
    }


def effective_helix_angle_deg(params: dict[str, Any] | None) -> float:
    """Return effective helix angle in degrees (0.0 when gear_type == 'spur')."""
    if not isinstance(params, dict):
        return 0.0
    gear_type = _to_choice(params.get("gear_type"), DEFAULT_PARAMS["gear_type"], VALID_GEAR_TYPES)
    if gear_type == "spur":
        return 0.0
    return _to_float(params.get("helix_angle_deg"), DEFAULT_PARAMS["helix_angle_deg"], 0.0, 60.0)


def normalize_params(raw: dict[str, Any] | None) -> dict[str, Any]:
    """Deep-copy DEFAULT_PARAMS, merge raw values, coerce types, and clamp bounds."""
    d = DEFAULT_PARAMS
    src = raw if isinstance(raw, dict) else {}

    raw_name = src.get("name", d["name"])
    if isinstance(raw_name, str) and raw_name.strip():
        clean_name = raw_name.strip()[:80]
    else:
        clean_name = str(d["name"])

    pinion = normalize_gear_body(
        src.get("pinion") if isinstance(src.get("pinion"), dict) else None,
        default_teeth=int(d["pinion"]["teeth"]),
        default_bore_type=str(d["pinion"]["bore_type"]),
        default_bore_mm=float(d["pinion"]["bore_diameter_mm"]),
        defaults_template=d["pinion"],
    )
    gear = normalize_gear_body(
        src.get("gear") if isinstance(src.get("gear"), dict) else None,
        default_teeth=int(d["gear"]["teeth"]),
        default_bore_type=str(d["gear"]["bore_type"]),
        default_bore_mm=float(d["gear"]["bore_diameter_mm"]),
        defaults_template=d["gear"],
    )

    return {
        "schema_version": SCHEMA_VERSION,
        "name": clean_name,
        "gear_type": _to_choice(src.get("gear_type"), d["gear_type"], VALID_GEAR_TYPES),
        "module_mm": _to_float(src.get("module_mm"), d["module_mm"], 0.5, 10.0),
        "pressure_angle_deg": _to_float(
            src.get("pressure_angle_deg"), d["pressure_angle_deg"], 14.5, 30.0
        ),
        "helix_angle_deg": _to_float(src.get("helix_angle_deg"), d["helix_angle_deg"], 0.0, 60.0),
        "helix_hand": _to_choice(src.get("helix_hand"), d["helix_hand"], VALID_HELIX_HANDS),
        "face_width_mm": _to_float(src.get("face_width_mm"), d["face_width_mm"], 2.0, 120.0),
        "addendum_coeff": _to_float(src.get("addendum_coeff"), d["addendum_coeff"], 0.40, 1.40),
        "clearance_coeff": _to_float(src.get("clearance_coeff"), d["clearance_coeff"], 0.10, 0.50),
        "root_fillet_coeff": _to_float(
            src.get("root_fillet_coeff"), d["root_fillet_coeff"], 0.05, 0.45
        ),
        "tip_chamfer_coeff": _to_float(
            src.get("tip_chamfer_coeff"), d["tip_chamfer_coeff"], 0.00, 0.25
        ),
        "auto_profile_shift": _to_bool(src.get("auto_profile_shift"), d["auto_profile_shift"]),
        "profile_shift_g1": _to_float(
            src.get("profile_shift_g1"), d["profile_shift_g1"], -0.50, 0.80
        ),
        "profile_shift_g2": _to_float(
            src.get("profile_shift_g2"), d["profile_shift_g2"], -0.50, 0.80
        ),
        "backlash_mm": _to_float(src.get("backlash_mm"), d["backlash_mm"], 0.00, 1.00),
        "xy_compensation_mm": _to_float(
            src.get("xy_compensation_mm"), d["xy_compensation_mm"], -0.20, 0.30
        ),
        "elephant_foot_chamfer_mm": _to_float(
            src.get("elephant_foot_chamfer_mm"), d["elephant_foot_chamfer_mm"], 0.00, 1.50
        ),
        "center_distance_offset_mm": _to_float(
            src.get("center_distance_offset_mm"), d["center_distance_offset_mm"], -1.50, 3.00
        ),
        "input_torque_nm": _to_float(src.get("input_torque_nm"), d["input_torque_nm"], 0.05, 50.0),
        "pinion": pinion,
        "gear": gear,
        "sim_rpm": _to_float(src.get("sim_rpm"), d["sim_rpm"], 1.0, 10.0),
        "sim_direction": _to_choice(src.get("sim_direction"), d["sim_direction"], VALID_SIM_DIRECTIONS),
        "export_target": _to_choice(src.get("export_target"), d["export_target"], VALID_EXPORT_TARGETS),
        "auto_configure_slicer": _to_bool(
            src.get("auto_configure_slicer"), d["auto_configure_slicer"]
        ),
    }

# ===========================================================================
# MODULE: gear_studio.involute_math
# ===========================================================================

"""ISO 21771 / ISO 53 transverse + normal involute gear geometry and 2D contour builders."""

pass  # [bundled] hoisted __future__ import

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
    pass  # [bundled] resolved intra-package import


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

# ===========================================================================
# MODULE: gear_studio.fit_and_kinematics
# ===========================================================================

"""Contact ratio, 2D polygon interference/jamming detection, kinematics, and FDM printability."""

pass  # [bundled] hoisted __future__ import

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
    pass  # [bundled] resolved intra-package import

if "compute_gear_pair_geometry" not in globals():
    pass  # [bundled] resolved intra-package import

PLA_DENSITY_G_CM3: float = 1.24


def _ctx_float(ctx: dict[str, Any], key: str, default: float, lo: float, hi: float) -> float:
    val = ctx.get(key, default)
    if isinstance(val, (list, tuple)) and len(val) > 0:
        val = val[0]
    if isinstance(val, str):
        val = val.strip().rstrip("%mM ").strip()
    try:
        f = float(val)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(f) or f <= 0.0:
        return default
    return max(lo, min(hi, f))


def _rotate_2d(pts: np.ndarray, angle_rad: float) -> np.ndarray:
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    out = np.empty_like(pts)
    out[:, 0] = pts[:, 0] * c - pts[:, 1] * s
    out[:, 1] = pts[:, 0] * s + pts[:, 1] * c
    return out


def _points_inside_star_ccw_polygon(
    query_pts: np.ndarray,
    poly_centered: np.ndarray,
) -> np.ndarray:
    """Return boolean mask of query_pts (in same local frame as poly_centered) strictly inside CCW star polygon."""
    if len(query_pts) == 0:
        return np.zeros(0, dtype=bool)

    angles = np.arctan2(poly_centered[:, 1], poly_centered[:, 0])
    start_idx = int(np.argmin(angles))
    p_rot = np.roll(poly_centered, -start_idx, axis=0)
    a_rot = np.roll(angles, -start_idx)

    # Ensure monotonic non-decreasing angles (handle tiny wrap numerical jitter if any)
    q_ang = np.arctan2(query_pts[:, 1], query_pts[:, 0])
    idx_hi = np.searchsorted(a_rot, q_ang, side="right")
    n = len(p_rot)
    i0 = (idx_hi - 1) % n
    i1 = idx_hi % n

    v0 = p_rot[i0]
    v1 = p_rot[i1]
    ex = v1[:, 0] - v0[:, 0]
    ey = v1[:, 1] - v0[:, 1]
    qx = query_pts[:, 0] - v0[:, 0]
    qy = query_pts[:, 1] - v0[:, 1]

    # For CCW star polygon around (0, 0), origin lies strictly on the left (cross > 0) of every edge v0 -> v1
    cross = ex * qy - ey * qx
    edge_len = np.hypot(ex, ey) + 1e-12
    signed_inward = cross / edge_len
    return signed_inward > 1e-6


def _point_to_segments_min_dist(pts: np.ndarray, s0: np.ndarray, s1: np.ndarray) -> np.ndarray:
    """Return (P,) array of minimum Euclidean distance from each point in `pts` (P, 2) to segments s0->s1 (S, 2)."""
    if len(pts) == 0 or len(s0) == 0:
        return np.full(len(pts), float("inf"), dtype=np.float64)

    seg_v = s1 - s0  # (S, 2)
    seg_len_sq = np.sum(seg_v * seg_v, axis=1)  # (S,)
    safe_len_sq = np.where(seg_len_sq > 1e-18, seg_len_sq, 1.0)

    # diff: (P, S, 2)
    diff = pts[:, None, :] - s0[None, :, :]
    t = (diff[:, :, 0] * seg_v[None, :, 0] + diff[:, :, 1] * seg_v[None, :, 1]) / safe_len_sq[None, :]
    t = np.clip(t, 0.0, 1.0)

    proj_x = s0[None, :, 0] + t * seg_v[None, :, 0]
    proj_y = s0[None, :, 1] + t * seg_v[None, :, 1]
    dx = pts[:, None, 0] - proj_x
    dy = pts[:, None, 1] - proj_y
    dist_sq = dx * dx + dy * dy
    return np.sqrt(np.min(dist_sq, axis=1))


def _segments_intersect_any(a0: np.ndarray, a1: np.ndarray, b0: np.ndarray, b1: np.ndarray) -> bool:
    """Vectorized 2D segment-segment intersection test between A (M1, 2) and B (M2, 2)."""
    if len(a0) == 0 or len(b0) == 0:
        return False

    # Bounding-box reject first
    a_min_x = np.minimum(a0[:, 0], a1[:, 0])[:, None]
    a_max_x = np.maximum(a0[:, 0], a1[:, 0])[:, None]
    b_min_x = np.minimum(b0[:, 0], b1[:, 0])[None, :]
    b_max_x = np.maximum(b0[:, 0], b1[:, 0])[None, :]

    a_min_y = np.minimum(a0[:, 1], a1[:, 1])[:, None]
    a_max_y = np.maximum(a0[:, 1], a1[:, 1])[:, None]
    b_min_y = np.minimum(b0[:, 1], b1[:, 1])[None, :]
    b_max_y = np.maximum(b0[:, 1], b1[:, 1])[None, :]

    bbox_hit = (a_max_x >= b_min_x - 1e-9) & (b_max_x >= a_min_x - 1e-9) & (
        a_max_y >= b_min_y - 1e-9
    ) & (b_max_y >= a_min_y - 1e-9)
    if not np.any(bbox_hit):
        return False

    ia, ib = np.nonzero(bbox_hit)
    pa0 = a0[ia]
    pa1 = a1[ia]
    pb0 = b0[ib]
    pb1 = b1[ib]

    da = pa1 - pa0
    db = pb1 - pb0

    def _cross2(u: np.ndarray, v: np.ndarray) -> np.ndarray:
        return u[:, 0] * v[:, 1] - u[:, 1] * v[:, 0]

    c1 = _cross2(da, pb0 - pa0)
    c2 = _cross2(da, pb1 - pa0)
    c3 = _cross2(db, pa0 - pb0)
    c4 = _cross2(db, pa1 - pb0)

    proper = (c1 * c2 < -1e-16) & (c3 * c4 < -1e-16)
    return bool(np.any(proper))


def evaluate_meshed_2d_clearance(
    params: dict[str, Any],
    steps: int = 9,
) -> dict[str, Any]:
    """Evaluate real 2D polygon clearance & collision between meshed G1 and G2 across sub-pitch steps."""
    p = normalize_params(params)
    geom = compute_gear_pair_geometry(p)

    z1 = int(geom["pinion"]["teeth"])
    z2 = int(geom["gear"]["teeth"])
    a = float(geom["center_distance_mm"])
    phase2 = float(geom["mesh_phase_g2_rad"])
    ra1 = float(geom["pinion"]["tip_radius_mm"])
    ra2 = float(geom["gear"]["tip_radius_mm"])
    m_t = float(geom["m_t"])

    if a >= ra1 + ra2 + 1e-6:
        sep = a - (ra1 + ra2)
        return {
            "min_clearance_mm": sep,
            "collision_detected": False,
            "disengaged": True,
        }

    poly1_base = build_gear_2d_contour(p, "pinion", samples_per_flank=11, radial_inset_mm=0.0)
    poly2_base = build_gear_2d_contour(p, "gear", samples_per_flank=11, radial_inset_mm=0.0)

    n_steps = max(3, int(steps))
    pitch_angle_1 = (2.0 * math.pi) / float(z1)

    min_signed_clearance = float("inf")
    any_collision = False

    cull_r2_sq = (ra2 + 2.5 * m_t) ** 2
    cull_r1_sq = (ra1 + 2.5 * m_t) ** 2

    for k in range(n_steps):
        theta1 = (float(k) / float(n_steps)) * pitch_angle_1
        phi2 = phase2 - theta1 * (float(z1) / float(z2))

        p1 = _rotate_2d(poly1_base, theta1)
        p2_centered = _rotate_2d(poly2_base, phi2)
        p2 = p2_centered.copy()
        p2[:, 0] += a

        a0 = p1
        a1 = np.roll(p1, -1, axis=0)
        b0 = p2
        b1 = np.roll(p2, -1, axis=0)

        # Cull to segments near the meshing zone between (0, 0) and (a, 0)
        d1_to_g2_sq = np.minimum(
            (a0[:, 0] - a) ** 2 + a0[:, 1] ** 2,
            (a1[:, 0] - a) ** 2 + a1[:, 1] ** 2,
        )
        d2_to_g1_sq = np.minimum(
            b0[:, 0] ** 2 + b0[:, 1] ** 2,
            b1[:, 0] ** 2 + b1[:, 1] ** 2,
        )

        act_a = d1_to_g2_sq <= cull_r2_sq
        act_b = d2_to_g1_sq <= cull_r1_sq
        if not (np.any(act_a) and np.any(act_b)):
            continue

        aa0 = a0[act_a]
        aa1 = a1[act_a]
        bb0 = b0[act_b]
        bb1 = b1[act_b]

        # Test vertices + edge midpoints for penetration into opposing star polygon
        cand1 = np.vstack((aa0, 0.5 * (aa0 + aa1)))
        cand1_in_g2_frame = cand1.copy()
        cand1_in_g2_frame[:, 0] -= a
        cand1_near = (
            cand1_in_g2_frame[:, 0] ** 2 + cand1_in_g2_frame[:, 1] ** 2
        ) < (ra2 * ra2)
        in_g2_mask = np.zeros(len(cand1), dtype=bool)
        if np.any(cand1_near):
            in_g2_mask[cand1_near] = _points_inside_star_ccw_polygon(
                cand1_in_g2_frame[cand1_near], p2_centered
            )

        cand2 = np.vstack((bb0, 0.5 * (bb0 + bb1)))
        cand2_near = (cand2[:, 0] ** 2 + cand2[:, 1] ** 2) < (ra1 * ra1)
        in_g1_mask = np.zeros(len(cand2), dtype=bool)
        if np.any(cand2_near):
            in_g1_mask[cand2_near] = _points_inside_star_ccw_polygon(cand2[cand2_near], p1)

        seg_cross = _segments_intersect_any(aa0, aa1, bb0, bb1)

        if seg_cross or np.any(in_g2_mask) or np.any(in_g1_mask):
            any_collision = True
            pen_d = 1e-4
            if np.any(in_g2_mask):
                d_pen1 = _point_to_segments_min_dist(cand1[in_g2_mask], bb0, bb1)
                pen_d = max(pen_d, float(np.max(d_pen1)))
            if np.any(in_g1_mask):
                d_pen2 = _point_to_segments_min_dist(cand2[in_g1_mask], aa0, aa1)
                pen_d = max(pen_d, float(np.max(d_pen2)))
            step_clear = -pen_d
        else:
            d_ab = _point_to_segments_min_dist(aa0, bb0, bb1)
            d_ba = _point_to_segments_min_dist(bb0, aa0, aa1)
            step_clear = min(float(np.min(d_ab)), float(np.min(d_ba)))

        if step_clear < min_signed_clearance:
            min_signed_clearance = step_clear

    if not math.isfinite(min_signed_clearance):
        min_signed_clearance = max(0.0, a - (ra1 + ra2))

    return {
        "min_clearance_mm": min_signed_clearance,
        "collision_detected": any_collision,
        "disengaged": False,
    }


def _estimate_single_gear_volume_cm3(
    body_cfg: dict[str, Any],
    g_geom: dict[str, Any],
    face_w_mm: float,
) -> float:
    """Analytical volume estimate (cm^3) used when pre-built MeshData objects are not passed in."""
    r_pitch = float(g_geom["pitch_radius_mm"])
    r_root = float(g_geom["root_radius_mm"])
    area_gear = math.pi * (r_pitch * r_pitch)

    if str(body_cfg["bore_type"]) != "none":
        r_bore = 0.5 * (float(body_cfg["bore_diameter_mm"]) + float(body_cfg["bore_clearance_mm"]))
        r_bore = min(r_bore, 0.85 * r_root)
        area_bore = math.pi * (r_bore * r_bore)
    else:
        r_bore = 0.0
        area_bore = 0.0

    vol_mm3 = max(10.0, (area_gear - area_bore) * face_w_mm)

    if body_cfg["hub_enabled"]:
        r_hub = min(0.5 * float(body_cfg["hub_diameter_mm"]), 0.90 * r_root)
        if r_hub > r_bore + 0.5:
            vol_mm3 += math.pi * (r_hub * r_hub - r_bore * r_bore) * float(body_cfg["hub_height_mm"])

    if body_cfg["recess_enabled"]:
        r_rec = min(0.5 * float(body_cfg["recess_diameter_mm"]), 0.88 * r_root)
        if r_rec > r_bore + 0.4:
            depth = min(float(body_cfg["recess_depth_mm"]), 0.42 * face_w_mm)
            sides = 2.0 if body_cfg["recess_side"] == "both" else 1.0
            vol_mm3 -= sides * math.pi * (r_rec * r_rec - r_bore * r_bore) * depth

    l_mode = str(body_cfg["lightening_mode"])
    r_web_in = max(r_bore + 2.0, 0.32 * r_root)
    r_web_out = 0.82 * r_root
    if l_mode == "web_recess" and r_web_out > r_web_in + 1.5:
        pocket_h = max(0.0, face_w_mm - float(body_cfg["web_thickness_mm"]))
        vol_mm3 -= math.pi * (r_web_out * r_web_out - r_web_in * r_web_in) * pocket_h
    elif l_mode == "lightening_holes" and r_web_out > r_web_in + 2.0:
        k_holes = int(body_cfg["lightening_hole_count"])
        r_hole = min(0.5 * float(body_cfg["lightening_hole_diameter_mm"]), 0.42 * (r_web_out - r_web_in))
        if r_hole > 0.5:
            vol_mm3 -= float(k_holes) * math.pi * (r_hole * r_hole) * face_w_mm

    return max(0.05, vol_mm3 / 1000.0)


def analyze_gear_pair(
    params: dict[str, Any],
    host_context: dict[str, Any] | None = None,
    meshes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Comprehensive engineering & FDM printability diagnostics for the parametric gear pair."""
    p = normalize_params(params)
    ctx = host_context if isinstance(host_context, dict) else {}
    geom = compute_gear_pair_geometry(p)

    bed_x = _ctx_float(ctx, "bed_x", 220.0, 50.0, 2000.0)
    bed_y = _ctx_float(ctx, "bed_y", 220.0, 50.0, 2000.0)
    line_w = _ctx_float(ctx, "line_width_mm", 0.42, 0.15, 2.5)
    layer_h = _ctx_float(ctx, "layer_height_mm", 0.20, 0.05, 1.0)

    gear_type = str(p["gear_type"])
    beta_deg = effective_helix_angle_deg(p)
    beta_rad = math.radians(beta_deg)
    cos_beta = math.cos(beta_rad)
    sin_beta = math.sin(beta_rad)

    m_n = float(geom["m_n"])
    m_t = float(geom["m_t"])
    alpha_t_rad = math.radians(float(geom["alpha_t_deg"]))
    cos_alpha_t = math.cos(alpha_t_rad)

    z1 = int(geom["pinion"]["teeth"])
    z2 = int(geom["gear"]["teeth"])
    z_sum = float(z1 + z2)

    a0 = float(geom["nominal_center_distance_mm"])
    a = float(geom["center_distance_mm"])
    min_non_jam_a = float(geom["min_non_jam_center_distance_mm"])
    delta_a = a - a0

    rb1 = float(geom["pinion"]["base_radius_mm"])
    rb2 = float(geom["gear"]["base_radius_mm"])
    ra1 = float(geom["pinion"]["tip_radius_mm"])
    ra2 = float(geom["gear"]["tip_radius_mm"])
    rf1 = float(geom["pinion"]["root_radius_mm"])
    rf2 = float(geom["gear"]["root_radius_mm"])
    rw1 = float(geom["pinion"]["working_pitch_radius_mm"])
    psi_b1 = float(geom["pinion"]["base_half_angle_rad"])
    psi_b2 = float(geom["gear"]["base_half_angle_rad"])
    face_w = float(p["face_width_mm"])

    # Operating pressure angle at actual center distance a
    cos_alpha_op = max(0.0, min(1.0, (rb1 + rb2) / max(1e-6, a)))
    alpha_op_rad = math.acos(cos_alpha_op)
    sin_alpha_op = math.sin(alpha_op_rad)
    tan_alpha_op = math.tan(alpha_op_rad) if cos_alpha_op > 1e-5 else 0.0

    # 1. Contact Ratios (ISO 21771)
    t1t2_len = a * sin_alpha_op
    disengaged = bool(a >= ra1 + ra2 - 1e-5)

    if disengaged:
        g_alpha = 0.0
        involute_base_interference = False
    else:
        seg_g1 = math.sqrt(max(0.0, ra1 * ra1 - rb1 * rb1))
        seg_g2 = math.sqrt(max(0.0, ra2 * ra2 - rb2 * rb2))
        # Base-tangent interference occurs if mating tip reaches beyond tangent point T1 or T2
        involute_base_interference = bool(
            (seg_g1 > t1t2_len + 0.02 * m_n) or (seg_g2 > t1t2_len + 0.02 * m_n)
        )
        g_alpha = max(0.0, min(seg_g1, t1t2_len) + min(seg_g2, t1t2_len) - t1t2_len)

    p_bt = math.pi * m_t * cos_alpha_t
    eps_alpha = g_alpha / max(1e-6, p_bt)

    if gear_type == "spur" or beta_deg <= 1e-6:
        eps_beta = 0.0
    elif gear_type == "herringbone":
        eps_beta = (0.5 * face_w * sin_beta) / (math.pi * m_n)
    else:
        eps_beta = (face_w * sin_beta) / (math.pi * m_n)

    eps_gamma = eps_alpha + eps_beta

    # 2. Fit, Backlash & Real 2D Polygon Clearance
    j_wt = (2.0 * a / z_sum) * (
        math.pi - float(z1) * psi_b1 - float(z2) * psi_b2 + z_sum * involute_fn(alpha_op_rad)
    )
    eff_backlash_mm = j_wt * cos_beta

    rad_clear_g1 = a - ra1 - rf2
    rad_clear_g2 = a - ra2 - rf1

    mesh_2d = evaluate_meshed_2d_clearance(p, steps=9)
    min_tooth_clear = float(mesh_2d["min_clearance_mm"])
    poly_collision = bool(mesh_2d["collision_detected"])

    jammed = bool(
        poly_collision
        or (a < min_non_jam_a - 1e-3)
        or (eff_backlash_mm < -1e-3)
        or (rad_clear_g1 < -1e-3)
        or (rad_clear_g2 < -1e-3)
    )
    interference_detected = bool(jammed or involute_base_interference)

    undercut_g1 = bool(geom["pinion"]["undercut"])
    undercut_g2 = bool(geom["gear"]["undercut"])
    thin_tip_limit = max(0.35, 0.22 * m_n)
    thin_tip_g1 = bool(float(geom["pinion"]["tip_thickness_mm"]) < thin_tip_limit)
    thin_tip_g2 = bool(float(geom["gear"]["tip_thickness_mm"]) < thin_tip_limit)

    # 3. Kinematics & Forces
    ratio = float(geom["ratio"])
    rpm_g1 = float(p["sim_rpm"])
    rpm_g2 = rpm_g1 / ratio
    omega_g1 = (2.0 * math.pi * rpm_g1) / 60.0
    v_pitch_mm_s = omega_g1 * rw1

    torque_g1 = float(p["input_torque_nm"])
    torque_g2 = torque_g1 * ratio

    # Tangential, radial, and net axial thrust forces at working pitch point
    f_tangential = (torque_g1 * 1000.0) / max(0.5, rw1)
    f_radial = f_tangential * tan_alpha_op
    axial_balanced = bool(gear_type in ("spur", "herringbone") or beta_deg <= 1e-6)
    f_axial = 0.0 if axial_balanced else f_tangential * math.tan(beta_rad)

    # 4. Printability, Bed Fit, Volume, Weight & Wall Loops
    helix_overhang_deg = 0.0 if gear_type == "spur" else beta_deg
    has_bottom_recess = bool(
        (p["pinion"]["recess_enabled"] and p["pinion"]["recess_side"] in ("bottom", "both"))
        or (p["gear"]["recess_enabled"] and p["gear"]["recess_side"] in ("bottom", "both"))
        or p["pinion"]["lightening_mode"] == "web_recess"
        or p["gear"]["lightening_mode"] == "web_recess"
    )
    supports_needed = bool(helix_overhang_deg > 48.0 or has_bottom_recess)

    gap_mm = 8.0
    d_out_1 = 2.0 * ra1
    d_out_2 = 2.0 * ra2
    h_1 = face_w + (float(p["pinion"]["hub_height_mm"]) if p["pinion"]["hub_enabled"] else 0.0)
    h_2 = face_w + (float(p["gear"]["hub_height_mm"]) if p["gear"]["hub_enabled"] else 0.0)

    fp_x = d_out_1 + gap_mm + d_out_2
    fp_y = max(d_out_1, d_out_2)
    fp_z = max(h_1, h_2)

    est_vol_cm3 = 0.0
    if isinstance(meshes, dict) and meshes:
        for m_obj in meshes.values():
            vol_attr = getattr(m_obj, "volume_cm3", None)
            if vol_attr is not None and math.isfinite(float(vol_attr)):
                est_vol_cm3 += max(0.0, float(vol_attr))
    if est_vol_cm3 <= 1e-4:
        est_vol_cm3 = _estimate_single_gear_volume_cm3(
            p["pinion"], geom["pinion"], face_w
        ) + _estimate_single_gear_volume_cm3(p["gear"], geom["gear"], face_w)

    # Account for ~55% effective solid fraction (4-6 solid tooth walls + 35% gyroid core)
    effective_printed_vol_cm3 = max(0.10, est_vol_cm3 * 0.72)
    est_weight_g = effective_printed_vol_cm3 * PLA_DENSITY_G_CM3
    # Realistic FDM volumetric flow (~7.5 mm^3/s average including perimeters/retractions)
    est_time_min = max(3.0, (effective_printed_vol_cm3 * 1000.0) / (7.5 * 60.0) * (0.20 / layer_h))

    rec_walls = int(max(4, min(6, round((1.8 * m_n) / (2.0 * line_w)))))

    fits_bed = bool(
        (fp_x <= bed_x + 1e-3 and fp_y <= bed_y + 1e-3)
        or (fp_y <= bed_x + 1e-3 and fp_x <= bed_y + 1e-3)
    )

    # 5. Bilingual Issues & Overall Status
    issues: list[dict[str, str]] = []

    if disengaged:
        issues.append(
            {
                "severity": "critical",
                "code": "TEETH_DISENGAGED",
                "pt": (
                    f"Engrenagens desacopladas (a = {a:.2f} mm >= r_a1 + r_a2 = {ra1 + ra2:.2f} mm). "
                    "Reduza o deslocamento de distancia entre centros."
                ),
                "en": (
                    f"Gears are disengaged (a = {a:.2f} mm >= r_a1 + r_a2 = {ra1 + ra2:.2f} mm). "
                    "Reduce center distance offset."
                ),
            }
        )
    elif jammed:
        issues.append(
            {
                "severity": "critical",
                "code": "GEAR_MESH_JAMMED",
                "pt": (
                    f"Travamento / colisao fisica detectada (a = {a:.2f} mm < minimo livre "
                    f"{min_non_jam_a:.2f} mm, folga 2D = {min_tooth_clear:.3f} mm). Aumente Δa ou a folga (backlash)."
                ),
                "en": (
                    f"Physical mesh lockup / collision detected (a = {a:.2f} mm < min non-jam "
                    f"{min_non_jam_a:.2f} mm, 2D clearance = {min_tooth_clear:.3f} mm). Increase Δa or backlash."
                ),
            }
        )
    elif interference_detected:
        issues.append(
            {
                "severity": "critical",
                "code": "INVOLUTE_INTERFERENCE",
                "pt": (
                    "Interferencia evolvente abaixo do circulo de base detectada. "
                    "Ative o Deslocamento de Perfil Automatico (x) ou reduza a altura do adendo."
                ),
                "en": (
                    "Involute base-circle interference detected. "
                    "Enable Auto Profile Shift (x) or reduce addendum coefficient."
                ),
            }
        )

    if not disengaged and eps_gamma < 1.0:
        issues.append(
            {
                "severity": "critical",
                "code": "LOW_CONTACT_RATIO_CRITICAL",
                "pt": (
                    f"Razao de contato total critica (ε_γ = {eps_gamma:.2f} < 1.00): perda de continuidade de giro."
                ),
                "en": (
                    f"Critical total contact ratio (ε_γ = {eps_gamma:.2f} < 1.00): loss of continuous mesh action."
                ),
            }
        )
    elif not disengaged and eps_gamma < 1.20:
        issues.append(
            {
                "severity": "warn",
                "code": "MARGINAL_CONTACT_RATIO",
                "pt": (
                    f"Razao de contato justa (ε_γ = {eps_gamma:.2f} < 1.20). "
                    "Considere engrenagem helicoidal ou mais dentes para giro mais silencioso."
                ),
                "en": (
                    f"Marginal contact ratio (ε_γ = {eps_gamma:.2f} < 1.20). "
                    "Consider helical teeth or higher tooth count for smoother operation."
                ),
            }
        )

    if not jammed and eff_backlash_mm < 0.05:
        issues.append(
            {
                "severity": "warn",
                "code": "TIGHT_FDM_BACKLASH",
                "pt": (
                    f"Folga efetiva muito baixa ({eff_backlash_mm:.2f} mm) para impressao FDM. "
                    "Recomenda-se >= 0.10 mm ou imprimir o Kit de Teste Rapido antes."
                ),
                "en": (
                    f"Effective backlash ({eff_backlash_mm:.2f} mm) is tight for FDM printing. "
                    "Recommend >= 0.10 mm or printing the Quick Fit-Test Kit first."
                ),
            }
        )

    if undercut_g1 or undercut_g2:
        which_lbl_pt = "Pinhao (G1) e Coroa (G2)" if (undercut_g1 and undercut_g2) else (
            "Pinhao (G1)" if undercut_g1 else "Coroa (G2)"
        )
        which_lbl_en = "Pinion (G1) and Gear (G2)" if (undercut_g1 and undercut_g2) else (
            "Pinion (G1)" if undercut_g1 else "Gear (G2)"
        )
        issues.append(
            {
                "severity": "warn",
                "code": "UNDERCUT_RISK",
                "pt": f"Risco de undercut na raiz de {which_lbl_pt}. Ative 'Auto Profile Shift' para reforcar o pe do dente.",
                "en": f"Root undercut risk on {which_lbl_en}. Enable 'Auto Profile Shift' to strengthen tooth root.",
            }
        )

    if thin_tip_g1 or thin_tip_g2:
        issues.append(
            {
                "severity": "warn",
                "code": "THIN_TOOTH_TIP",
                "pt": (
                    f"Topo do dente fino (< {thin_tip_limit:.2f} mm) para bico FDM. "
                    "Reduza o deslocamento de perfil ou o fator de adendo."
                ),
                "en": (
                    f"Thin tooth tip (< {thin_tip_limit:.2f} mm) for FDM nozzle extrusion. "
                    "Reduce profile shift or addendum coefficient."
                ),
            }
        )

    if helix_overhang_deg > 48.0:
        issues.append(
            {
                "severity": "warn",
                "code": "HELIX_OVERHANG_HIGH",
                "pt": (
                    f"Angulo de helice elevado ({helix_overhang_deg:.1f}° > 48°): pode exigir suportes ou camadas finas (0.12 mm)."
                ),
                "en": (
                    f"Steep helix overhang ({helix_overhang_deg:.1f}° > 48°): may require supports or thin layers (0.12 mm)."
                ),
            }
        )
    elif has_bottom_recess:
        issues.append(
            {
                "severity": "warn",
                "code": "BOTTOM_RECESS_BRIDGE",
                "pt": "Rebaixo na face inferior detectado — verifique pontes/suportes no fatiador.",
                "en": "Bottom-side recess detected — verify bridging or enable supports in slicer.",
            }
        )

    if gear_type == "helical" and f_axial > 8.0:
        issues.append(
            {
                "severity": "info",
                "code": "AXIAL_THRUST_NOTICE",
                "pt": (
                    f"Empuxo axial lateral de {f_axial:.1f} N na helice simples. "
                    "Use encosto axial ou mude para Espinha de Peixe (Herringbone) para anular o empuxo (0 N)."
                ),
                "en": (
                    f"Unbalanced axial thrust of {f_axial:.1f} N on single helical gear. "
                    "Use thrust washers or switch to Herringbone to cancel axial thrust (0 N)."
                ),
            }
        )

    if not fits_bed:
        issues.append(
            {
                "severity": "critical",
                "code": "BED_OVERFLOW",
                "pt": (
                    f"Par lado a lado ({fp_x:.1f} x {fp_y:.1f} mm) excede a mesa ({bed_x:.0f} x {bed_y:.0f} mm). "
                    "Exporte Pinhao e Coroa separadamente."
                ),
                "en": (
                    f"Side-by-side pair ({fp_x:.1f} x {fp_y:.1f} mm) exceeds build plate ({bed_x:.0f} x {bed_y:.0f} mm). "
                    "Export Pinion and Gear individually."
                ),
            }
        )

    has_critical = any(it["severity"] == "critical" for it in issues)
    has_warn = any(it["severity"] == "warn" for it in issues)
    status = "critical" if has_critical else ("warn" if has_warn else "ok")

    return {
        "status": status,
        "geometry": geom,
        "contact": {
            "transverse_ratio": round(eps_alpha, 4),
            "axial_overlap_ratio": round(eps_beta, 4),
            "total_contact_ratio": round(eps_gamma, 4),
            "line_of_action_length_mm": round(g_alpha, 4),
        },
        "fit": {
            "effective_backlash_mm": round(eff_backlash_mm, 4),
            "radial_clearance_g1_mm": round(rad_clear_g1, 4),
            "radial_clearance_g2_mm": round(rad_clear_g2, 4),
            "min_tooth_clearance_mm": round(min_tooth_clear, 4),
            "interference_detected": interference_detected,
            "jammed": jammed,
            "undercut_g1": undercut_g1,
            "undercut_g2": undercut_g2,
            "thin_tip_g1": thin_tip_g1,
            "thin_tip_g2": thin_tip_g2,
            "center_distance_mm": round(a, 4),
            "nominal_center_distance_mm": round(a0, 4),
            "min_non_jam_center_distance_mm": round(min_non_jam_a, 4),
            "delta_a_mm": round(delta_a, 4),
        },
        "kinematics": {
            "ratio": round(ratio, 4),
            "rpm_g1": round(rpm_g1, 2),
            "rpm_g2": round(rpm_g2, 2),
            "pitch_line_velocity_mm_s": round(v_pitch_mm_s, 3),
            "torque_g1_nm": round(torque_g1, 4),
            "torque_g2_nm": round(torque_g2, 4),
            "tangential_force_n": round(f_tangential, 3),
            "radial_force_n": round(f_radial, 3),
            "axial_force_n": round(f_axial, 3),
            "axial_thrust_balanced": axial_balanced,
        },
        "printability": {
            "helix_overhang_deg": round(helix_overhang_deg, 1),
            "supports_needed": supports_needed,
            "fits_bed": fits_bed,
            "bed_x_mm": round(bed_x, 1),
            "bed_y_mm": round(bed_y, 1),
            "pair_footprint_mm": [round(fp_x, 2), round(fp_y, 2), round(fp_z, 2)],
            "estimated_volume_cm3": round(est_vol_cm3, 2),
            "estimated_weight_g": round(est_weight_g, 1),
            "estimated_print_time_min": round(est_time_min, 1),
            "recommended_wall_loops": rec_walls,
        },
        "issues": issues,
    }

# ===========================================================================
# MODULE: gear_studio.mesh_generator
# ===========================================================================

"""Strict 2-manifold 3D gear and Fit-Test Kit mesh generator for Orca Gear Studio."""

pass  # [bundled] hoisted __future__ import

from dataclasses import dataclass
import math
from typing import Any, Sequence

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
    pass  # [bundled] resolved intra-package import

if "compute_gear_pair_geometry" not in globals():
    pass  # [bundled] resolved intra-package import


@dataclass
class MeshData:
    vertices: np.ndarray            # (V, 3), float32, finite, min(Z) == 0.0, XY centered near (0, 0)
    triangles: np.ndarray           # (F, 3), int32, strict CCW outward winding
    face_normals: np.ndarray        # (F, 3), float32, unit vectors aligned > 0.99 with CCW cross product
    bounds_mm: dict[str, list[float]]  # {"min": [x,y,z], "max": [x,y,z], "size": [dx,dy,dz]}
    volume_cm3: float               # positive signed divergence volume in cm^3
    overhang_angles_deg: np.ndarray  # (F,), float32, downward overhang angle in degrees


# ---------------------------------------------------------------------------
# Mesh Finalization & Topological Builders
# ---------------------------------------------------------------------------


def _finalize_mesh(
    vertices: np.ndarray,
    triangles: np.ndarray,
    *,
    center_xy: bool = False,
) -> MeshData:
    """Finalize raw float64 vertices & int32 CCW triangles into a validated MeshData."""
    verts64 = np.asarray(vertices, dtype=np.float64).copy()
    tris = np.asarray(triangles, dtype=np.int32).reshape(-1, 3).copy()

    if len(verts64) == 0 or len(tris) == 0:
        empty_v = np.zeros((0, 3), dtype=np.float32)
        empty_t = np.zeros((0, 3), dtype=np.int32)
        empty_o = np.zeros((0,), dtype=np.float32)
        return MeshData(
            vertices=empty_v,
            triangles=empty_t,
            face_normals=empty_v.copy(),
            bounds_mm={"min": [0.0, 0.0, 0.0], "max": [0.0, 0.0, 0.0], "size": [0.0, 0.0, 0.0]},
            volume_cm3=0.0,
            overhang_angles_deg=empty_o,
        )

    if center_xy:
        mid_x = 0.5 * float(verts64[:, 0].min() + verts64[:, 0].max())
        mid_y = 0.5 * float(verts64[:, 1].min() + verts64[:, 1].max())
        verts64[:, 0] -= mid_x
        verts64[:, 1] -= mid_y

    z_min64 = float(verts64[:, 2].min())
    verts64[:, 2] -= z_min64
    verts64[np.abs(verts64[:, 2]) < 1e-7, 2] = 0.0

    verts32 = verts64.astype(np.float32)
    z_min32 = float(verts32[:, 2].min())
    if z_min32 != 0.0:
        verts32[:, 2] -= np.float32(z_min32)
    verts32[np.abs(verts32[:, 2]) < 1e-7, 2] = np.float32(0.0)

    v0 = verts32[tris[:, 0]].astype(np.float64)
    v1 = verts32[tris[:, 1]].astype(np.float64)
    v2 = verts32[tris[:, 2]].astype(np.float64)

    cross = np.cross(v1 - v0, v2 - v0)
    norms = np.linalg.norm(cross, axis=1, keepdims=True)
    unit_normals64 = cross / np.maximum(norms, 1e-30)
    face_normals = unit_normals64.astype(np.float32)

    signed_vol_mm3 = float(np.sum(np.einsum("ij,ij->i", v0, cross)) / 6.0)
    volume_cm3 = float(signed_vol_mm3 / 1000.0)

    # Downward overhang angle in degrees (0 deg for vertical/upward or bed-resting faces at Z == 0)
    face_z_max = np.maximum(np.maximum(v0[:, 2], v1[:, 2]), v2[:, 2])
    nz = unit_normals64[:, 2]
    overhang64 = np.zeros(len(tris), dtype=np.float64)
    down_mask = (face_z_max > 1e-3) & (nz < -1e-5)
    if np.any(down_mask):
        overhang64[down_mask] = np.degrees(np.arcsin(np.clip(-nz[down_mask], 0.0, 1.0)))
    overhang_angles_deg = overhang64.astype(np.float32)

    vmin = verts32.min(axis=0)
    vmax = verts32.max(axis=0)
    vsize = vmax - vmin
    bounds_mm = {
        "min": [float(vmin[0]), float(vmin[1]), float(vmin[2])],
        "max": [float(vmax[0]), float(vmax[1]), float(vmax[2])],
        "size": [float(vsize[0]), float(vsize[1]), float(vsize[2])],
    }

    return MeshData(
        vertices=verts32,
        triangles=tris,
        face_normals=face_normals,
        bounds_mm=bounds_mm,
        volume_cm3=volume_cm3,
        overhang_angles_deg=overhang_angles_deg,
    )


class _GearMeshBuilder:
    """Indexed vertex & CCW triangle accumulator guaranteeing zero accidental vertex collisions."""

    def __init__(self) -> None:
        self._verts_chunks: list[np.ndarray] = []
        self._tris_chunks: list[np.ndarray] = []
        self._v_count: int = 0

    def add_vertices(self, pts: np.ndarray) -> np.ndarray:
        arr = np.asarray(pts, dtype=np.float64)
        if arr.ndim == 1:
            arr = arr[None, :]
        n = arr.shape[0]
        start = self._v_count
        self._verts_chunks.append(arr)
        self._v_count += n
        return np.arange(start, start + n, dtype=np.int32)

    def add_vertex(self, x: float, y: float, z: float) -> int:
        idx = self._v_count
        self._verts_chunks.append(np.array([[x, y, z]], dtype=np.float64))
        self._v_count += 1
        return idx

    def add_ring_2d(self, xy: np.ndarray, z: float) -> np.ndarray:
        xy64 = np.asarray(xy, dtype=np.float64)
        pts = np.column_stack((xy64[:, 0], xy64[:, 1], np.full(len(xy64), float(z), dtype=np.float64)))
        return self.add_vertices(pts)

    def add_polar_ring(self, radii: np.ndarray | float, thetas: np.ndarray, z: float) -> np.ndarray:
        r_arr = np.broadcast_to(np.asarray(radii, dtype=np.float64), thetas.shape)
        pts = np.column_stack((
            r_arr * np.cos(thetas),
            r_arr * np.sin(thetas),
            np.full(len(thetas), float(z), dtype=np.float64),
        ))
        return self.add_vertices(pts)

    def add_circle_ring(
        self,
        cx: float,
        cy: float,
        radius: float,
        z: float,
        count: int,
        phase_rad: float = 0.0,
    ) -> np.ndarray:
        phis = phase_rad + np.linspace(0.0, 2.0 * math.pi, count, endpoint=False, dtype=np.float64)
        pts = np.column_stack((
            cx + radius * np.cos(phis),
            cy + radius * np.sin(phis),
            np.full(count, float(z), dtype=np.float64),
        ))
        return self.add_vertices(pts)

    def add_triangles(self, tris: np.ndarray | Sequence[tuple[int, int, int]]) -> None:
        arr = np.asarray(tris, dtype=np.int32)
        if arr.size > 0:
            self._tris_chunks.append(arr.reshape(-1, 3))

    def add_quad_strip(self, ring_a: np.ndarray, ring_b: np.ndarray, reverse: bool = False) -> None:
        """Connect two equal-length closed CCW rings.

        With reverse=False, normal is (+dz * r_hat - dr * z_hat):
        - upward outer wall (dz > 0, dr == 0) -> +r_hat (outward)
        - outward bottom cap (dr > 0, dz == 0) -> -z_hat (downward)
        With reverse=True, normal is (-dz * r_hat + dr * z_hat):
        - upward inner bore/hole tunnel (dz > 0, dr == 0) -> -r_hat (inward into hole)
        - outward top cap (dr > 0, dz == 0) -> +z_hat (upward)
        """
        a0 = np.asarray(ring_a, dtype=np.int32)
        a1 = np.roll(a0, -1)
        b0 = np.asarray(ring_b, dtype=np.int32)
        b1 = np.roll(b0, -1)
        if not reverse:
            t1 = np.column_stack((a0, a1, b1))
            t2 = np.column_stack((a0, b1, b0))
        else:
            t1 = np.column_stack((a0, b1, a1))
            t2 = np.column_stack((a0, b0, b1))
        self.add_triangles(np.vstack((t1, t2)))

    def add_tube_grid(self, rings: Sequence[np.ndarray], reverse: bool = False) -> None:
        arr = np.asarray(rings, dtype=np.int32)
        a0 = arr[:-1, :]
        a1 = np.roll(a0, -1, axis=1)
        b0 = arr[1:, :]
        b1 = np.roll(b0, -1, axis=1)
        if not reverse:
            t1 = np.stack((a0, a1, b1), axis=-1).reshape(-1, 3)
            t2 = np.stack((a0, b1, b0), axis=-1).reshape(-1, 3)
        else:
            t1 = np.stack((a0, b1, a1), axis=-1).reshape(-1, 3)
            t2 = np.stack((a0, b0, b1), axis=-1).reshape(-1, 3)
        self.add_triangles(np.vstack((t1, t2)))

    def add_disk_fan(self, center_idx: int, ring: np.ndarray, normal_up: bool = True) -> None:
        r0 = np.asarray(ring, dtype=np.int32)
        m = len(r0)
        c = np.full(m, int(center_idx), dtype=np.int32)
        r1 = np.roll(r0, -1)
        if normal_up:
            tris = np.column_stack((c, r0, r1))
        else:
            tris = np.column_stack((c, r1, r0))
        self.add_triangles(tris)

    def get_vertices_array(self) -> np.ndarray:
        if not self._verts_chunks:
            return np.zeros((0, 3), dtype=np.float64)
        return np.vstack(self._verts_chunks)

    def build(self, *, center_xy: bool = False) -> MeshData:
        verts64 = self.get_vertices_array()
        tris = (
            np.vstack(self._tris_chunks).astype(np.int32)
            if self._tris_chunks
            else np.zeros((0, 3), dtype=np.int32)
        )
        return _finalize_mesh(verts64, tris, center_xy=center_xy)


# ---------------------------------------------------------------------------
# 2D Loop Bridging & Exact Polygon-With-Holes Ear-Clipping
# ---------------------------------------------------------------------------


def _mg_bridge_convex_loops_up(
    verts_xy: np.ndarray,
    loop_in: Sequence[int] | np.ndarray,
    loop_out: Sequence[int] | np.ndarray,
    center_xy: tuple[float, float],
) -> np.ndarray:
    """Triangulate annulus between two strictly convex/circular CCW loops around center_xy (+Z normal)."""
    lin = [int(i) for i in loop_in]
    lout = [int(i) for i in loop_out]
    m1 = len(lin)
    m2 = len(lout)
    cx, cy = center_xy

    ang_in: list[float] = []
    for p, idx in enumerate(lin):
        a = math.atan2(float(verts_xy[idx, 1]) - cy, float(verts_xy[idx, 0]) - cx)
        if p > 0:
            while a <= ang_in[-1]:
                a += 2.0 * math.pi
        ang_in.append(a)
    ang_in.append(ang_in[0] + 2.0 * math.pi)

    raw_out = [
        math.atan2(float(verts_xy[idx, 1]) - cy, float(verts_xy[idx, 0]) - cx)
        for idx in lout
    ]
    best_s = min(
        range(m2),
        key=lambda s: abs(((raw_out[s] - ang_in[0] + math.pi) % (2.0 * math.pi)) - math.pi),
    )
    lout = lout[best_s:] + lout[:best_s]

    a0 = math.atan2(float(verts_xy[lout[0], 1]) - cy, float(verts_xy[lout[0], 0]) - cx)
    while a0 - ang_in[0] > math.pi:
        a0 -= 2.0 * math.pi
    while ang_in[0] - a0 > math.pi:
        a0 += 2.0 * math.pi

    ang_out: list[float] = [a0]
    for q in range(1, m2):
        idx = lout[q]
        a = math.atan2(float(verts_xy[idx, 1]) - cy, float(verts_xy[idx, 0]) - cx)
        while a <= ang_out[-1]:
            a += 2.0 * math.pi
        ang_out.append(a)
    ang_out.append(ang_out[0] + 2.0 * math.pi)

    tris: list[tuple[int, int, int]] = []
    p = 0
    q = 0
    while p < m1 or q < m2:
        if p == m1:
            advance_out = True
        elif q == m2:
            advance_out = False
        else:
            skew_if_in = abs(ang_in[p + 1] - ang_out[q])
            skew_if_out = abs(ang_out[q + 1] - ang_in[p])
            advance_out = skew_if_out < skew_if_in

        if advance_out:
            tris.append((lin[p % m1], lout[q % m2], lout[(q + 1) % m2]))
            q += 1
        else:
            tris.append((lin[p % m1], lout[q % m2], lin[(p + 1) % m1]))
            p += 1

    return np.asarray(tris, dtype=np.int32)


def _mg_cross2d(
    ax: float,
    ay: float,
    bx: float,
    by: float,
    cx: float,
    cy: float,
) -> float:
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)


def _mg_signed_area_2d(pts_xy: np.ndarray, indices: Sequence[int]) -> float:
    n = len(indices)
    area2 = 0.0
    for i in range(n):
        u = indices[i]
        v = indices[(i + 1) % n]
        area2 += float(pts_xy[u, 0] * pts_xy[v, 1] - pts_xy[v, 0] * pts_xy[u, 1])
    return 0.5 * area2


def _mg_point_in_tri_2d(
    px: float,
    py: float,
    ax: float,
    ay: float,
    bx: float,
    by: float,
    cx: float,
    cy: float,
    eps: float = -1e-10,
) -> bool:
    c1 = _mg_cross2d(ax, ay, bx, by, px, py)
    if c1 < eps:
        return False
    c2 = _mg_cross2d(bx, by, cx, cy, px, py)
    if c2 < eps:
        return False
    c3 = _mg_cross2d(cx, cy, ax, ay, px, py)
    return c3 >= eps


def _mg_find_hole_bridge_pos(
    pts_xy: np.ndarray,
    poly: list[int],
    mx: float,
    my: float,
) -> int:
    """Find a vertex position in `poly` strictly visible from rightmost hole vertex (mx, my)."""
    n = len(poly)
    y_span = max(1.0, float(pts_xy[poly, 1].max() - pts_xy[poly, 1].min()))
    my_ray = my
    if any(abs(float(pts_xy[v, 1]) - my_ray) < 1e-10 for v in poly):
        my_ray = my + 1.37e-8 * y_span

    best_x = float("inf")
    best_edge = -1
    for i in range(n):
        u = poly[i]
        v = poly[(i + 1) % n]
        ux, uy = float(pts_xy[u, 0]), float(pts_xy[u, 1])
        vx, vy = float(pts_xy[v, 0]), float(pts_xy[v, 1])
        if (uy > my_ray) != (vy > my_ray):
            x_int = ux + (my_ray - uy) * (vx - ux) / (vy - uy)
            if x_int > mx and x_int < best_x:
                best_x = x_int
                best_edge = i

    if best_edge < 0:
        return max(range(n), key=lambda k: float(pts_xy[poly[k], 0]))

    i0 = best_edge
    i1 = (best_edge + 1) % n
    cand_pos = i0 if float(pts_xy[poly[i0], 0]) >= float(pts_xy[poly[i1], 0]) else i1
    px, py = float(pts_xy[poly[cand_pos], 0]), float(pts_xy[poly[cand_pos], 1])

    if abs(py - my) <= 1e-10:
        return cand_pos

    # Triangle between M=(mx, my), ray hit I=(best_x, my), and candidate vertex P=(px, py)
    if py > my:
        tax, tay, tbx, tby, tcx, tcy = mx, my, best_x, my, px, py
    else:
        tax, tay, tbx, tby, tcx, tcy = mx, my, px, py, best_x, my

    best_reflex_pos = -1
    best_tan = float("inf")
    best_dist_sq = float("inf")

    cand_vid = poly[cand_pos]
    for k in range(n):
        vid = poly[k]
        if vid == cand_vid:
            continue
        prev_v = poly[k - 1]
        next_v = poly[(k + 1) % n]
        # Only reflex vertices can block visibility
        if _mg_cross2d(
            float(pts_xy[prev_v, 0]),
            float(pts_xy[prev_v, 1]),
            float(pts_xy[vid, 0]),
            float(pts_xy[vid, 1]),
            float(pts_xy[next_v, 0]),
            float(pts_xy[next_v, 1]),
        ) > 1e-11:
            continue
        kx, ky = float(pts_xy[vid, 0]), float(pts_xy[vid, 1])
        if kx < mx:
            continue
        if _mg_point_in_tri_2d(kx, ky, tax, tay, tbx, tby, tcx, tcy, eps=-1e-11):
            dx = kx - mx
            dy = abs(ky - my)
            tan_val = dy / max(dx, 1e-12)
            d2 = dx * dx + dy * dy
            if tan_val < best_tan - 1e-12 or (abs(tan_val - best_tan) <= 1e-12 and d2 < best_dist_sq):
                best_tan = tan_val
                best_dist_sq = d2
                best_reflex_pos = k

    return best_reflex_pos if best_reflex_pos >= 0 else cand_pos


def _mg_triangulate_cell_2d(
    pts_xy: np.ndarray,
    outer_loop: Sequence[int],
    hole_loops: Sequence[Sequence[int]] = (),
) -> np.ndarray:
    """Triangulate a 2D simple polygon (with 0 or more inner CCW hole loops) into +Z CCW triangles.

    Preserves exact input vertex indices along all outer and hole loops with zero T-junctions
    and guarantees strict 2-manifold directed edge pairing.
    """
    poly = [int(i) for i in outer_loop]
    if _mg_signed_area_2d(pts_xy, poly) < 0.0:
        poly.reverse()

    # Sort holes descending by maximum X so horizontal +X visibility rays never hit unmerged holes
    prepared_holes: list[tuple[float, list[int]]] = []
    for h in hole_loops:
        h_list = [int(i) for i in h]
        if len(h_list) < 3:
            continue
        if _mg_signed_area_2d(pts_xy, h_list) < 0.0:
            h_list.reverse()
        h_cw = h_list[::-1]
        max_x = max(float(pts_xy[v, 0]) for v in h_cw)
        prepared_holes.append((max_x, h_cw))

    prepared_holes.sort(key=lambda item: item[0], reverse=True)

    for _, h_cw in prepared_holes:
        m_idx = max(
            range(len(h_cw)),
            key=lambda idx: (float(pts_xy[h_cw[idx], 0]), float(pts_xy[h_cw[idx], 1])),
        )
        h_rot = h_cw[m_idx:] + h_cw[:m_idx]
        m_vid = h_rot[0]
        mx, my = float(pts_xy[m_vid, 0]), float(pts_xy[m_vid, 1])
        v_pos = _mg_find_hole_bridge_pos(pts_xy, poly, mx, my)
        v_vid = poly[v_pos]
        poly = poly[: v_pos + 1] + h_rot + [m_vid, v_vid] + poly[v_pos + 1 :]

    used_undirected: set[tuple[int, int]] = set()
    for i in range(len(poly)):
        u = poly[i]
        v = poly[(i + 1) % len(poly)]
        if u != v:
            used_undirected.add((min(u, v), max(u, v)))

    tris: list[tuple[int, int, int]] = []
    guard = len(poly) * 4 + 16

    while len(poly) > 3 and guard > 0:
        guard -= 1
        m = len(poly)
        best_k = -1
        best_quality = -1.0

        for tol in (1e-8, 1e-12):
            for k in range(m):
                ia = poly[k - 1]
                ib = poly[k]
                ic = poly[(k + 1) % m]
                if ia == ib or ib == ic or ia == ic:
                    continue
                chord = (min(ia, ic), max(ia, ic))
                if chord in used_undirected:
                    continue

                ax, ay = float(pts_xy[ia, 0]), float(pts_xy[ia, 1])
                bx, by = float(pts_xy[ib, 0]), float(pts_xy[ib, 1])
                cx, cy = float(pts_xy[ic, 0]), float(pts_xy[ic, 1])

                area2 = _mg_cross2d(ax, ay, bx, by, cx, cy)
                if area2 <= tol:
                    continue

                contains_other = False
                for p_vid in poly:
                    if p_vid == ia or p_vid == ib or p_vid == ic:
                        continue
                    if _mg_point_in_tri_2d(
                        float(pts_xy[p_vid, 0]),
                        float(pts_xy[p_vid, 1]),
                        ax,
                        ay,
                        bx,
                        by,
                        cx,
                        cy,
                        eps=-1e-10,
                    ):
                        contains_other = True
                        break
                if contains_other:
                    continue

                e2 = (
                    (bx - ax) ** 2 + (by - ay) ** 2
                    + (cx - bx) ** 2 + (cy - by) ** 2
                    + (ax - cx) ** 2 + (ay - cy) ** 2
                )
                quality = area2 / max(e2, 1e-30)
                if quality > best_quality:
                    best_quality = quality
                    best_k = k

            if best_k >= 0:
                break

        if best_k < 0:
            # Emergency convex fallback without chord constraint if polygon collapsed near 4 nodes
            for k in range(m):
                ia = poly[k - 1]
                ib = poly[k]
                ic = poly[(k + 1) % m]
                if ia == ib or ib == ic or ia == ic:
                    continue
                area2 = _mg_cross2d(
                    float(pts_xy[ia, 0]),
                    float(pts_xy[ia, 1]),
                    float(pts_xy[ib, 0]),
                    float(pts_xy[ib, 1]),
                    float(pts_xy[ic, 0]),
                    float(pts_xy[ic, 1]),
                )
                if area2 > 1e-13:
                    best_k = k
                    break
            if best_k < 0:
                break

        ia = poly[best_k - 1]
        ib = poly[best_k]
        ic = poly[(best_k + 1) % m]
        tris.append((ia, ib, ic))
        used_undirected.add((min(ia, ic), max(ia, ic)))
        poly.pop(best_k)

    if len(poly) == 3 and poly[0] != poly[1] and poly[1] != poly[2] and poly[2] != poly[0]:
        tris.append((poly[0], poly[1], poly[2]))

    return np.asarray(tris, dtype=np.int32)


# ---------------------------------------------------------------------------
# Public Gear Mesh Generator
# ---------------------------------------------------------------------------


def _mg_rotate_2d(xy: np.ndarray, angle_rad: float) -> np.ndarray:
    if abs(angle_rad) < 1e-12:
        return xy.copy()
    c = math.cos(angle_rad)
    s = math.sin(angle_rad)
    out = np.empty_like(xy)
    out[:, 0] = xy[:, 0] * c - xy[:, 1] * s
    out[:, 1] = xy[:, 0] * s + xy[:, 1] * c
    return out


def _mg_build_outer_z_schedule(
    face_width_mm: float,
    beta_deg: float,
    gear_type: str,
    chamfer_mm: float,
    resolution: str,
) -> tuple[list[float], list[float]]:
    """Build Z slice levels and corresponding radial insets for spur/helical/herringbone gears."""
    b = float(face_width_mm)
    gt = str(gear_type).strip().lower()
    has_chamfer = chamfer_mm > 0.03

    z_lo = chamfer_mm if has_chamfer else 0.0
    z_hi = (b - chamfer_mm) if has_chamfer else b
    span_mid = max(0.2, z_hi - z_lo)

    if gt == "spur" or abs(beta_deg) < 1e-4:
        if has_chamfer:
            return [0.0, z_lo, z_hi, b], [chamfer_mm, 0.0, 0.0, chamfer_mm]
        return [0.0, b], [0.0, 0.0]

    if resolution == "high":
        n_mid = int(round(max(24.0, min(56.0, 16.0 + 0.85 * b + 0.35 * abs(beta_deg)))))
    else:
        n_mid = int(round(max(16.0, min(28.0, 10.0 + 0.45 * b + 0.20 * abs(beta_deg)))))

    max_by_dz = max(2, int(math.floor(span_mid / 0.12)))
    n_mid = min(n_mid, max_by_dz)
    if n_mid % 2 == 1:
        n_mid = max(2, n_mid + 1 if n_mid + 1 <= max_by_dz else n_mid - 1)
    n_mid = max(2, n_mid)

    z_mid = np.linspace(z_lo, z_hi, n_mid + 1, dtype=np.float64).tolist()
    if gt == "herringbone":
        z_mid[n_mid // 2] = 0.5 * b

    if has_chamfer:
        z_levels = [0.0, *z_mid, b]
        insets = [chamfer_mm, *([0.0] * len(z_mid)), chamfer_mm]
    else:
        z_levels = z_mid
        insets = [0.0] * len(z_mid)

    return z_levels, insets


def _mg_add_k_hole_sectors(
    mb: _GearMeshBuilder,
    in_top_ring: np.ndarray,
    out_top_ring: np.ndarray,
    in_bot_ring: np.ndarray,
    out_bot_ring: np.ndarray,
    ring_thetas: np.ndarray,
    r_ann_in: float,
    r_ann_out: float,
    z_bot_h: float,
    z_top_h: float,
    k_holes: int,
    s_arc: int,
    req_hole_diam_mm: float,
    resolution: str,
) -> None:
    """Connect top & bottom annular sector rings [r_ann_in, r_ann_out] with K strict 2-manifold through-holes."""
    m_ang = k_holes * s_arc
    dpsi = math.pi / float(k_holes)
    r_hole_ring = 0.5 * (r_ann_in + r_ann_out)
    half_radial = 0.5 * (r_ann_out - r_ann_in)
    spoke_dist = r_hole_ring * math.sin(dpsi) if k_holes >= 2 else half_radial
    min_margin = min(0.75, 0.22 * min(half_radial, spoke_dist))
    max_r_h = max(0.22, min(half_radial - min_margin, spoke_dist - min_margin))
    r_h = max(0.22, min(0.5 * float(req_hole_diam_mm), max_r_h))

    n_spoke_mid = 5 if resolution == "high" else 3
    m_hole = 28 if resolution == "high" else 20

    spoke_r_mid = np.linspace(r_ann_in, r_ann_out, n_spoke_mid + 2, dtype=np.float64)[1:-1]

    spokes_top: list[np.ndarray] = []
    spokes_bot: list[np.ndarray] = []
    for k in range(k_holes):
        ang = float(ring_thetas[k * s_arc])
        ca = math.cos(ang)
        sa = math.sin(ang)
        mid_xy = np.column_stack((spoke_r_mid * ca, spoke_r_mid * sa))
        mid_t = mb.add_ring_2d(mid_xy, z_top_h)
        mid_b = mb.add_ring_2d(mid_xy, z_bot_h)
        spokes_top.append(
            np.concatenate((
                np.array([in_top_ring[k * s_arc]], dtype=np.int32),
                mid_t,
                np.array([out_top_ring[k * s_arc]], dtype=np.int32),
            ))
        )
        spokes_bot.append(
            np.concatenate((
                np.array([in_bot_ring[k * s_arc]], dtype=np.int32),
                mid_b,
                np.array([out_bot_ring[k * s_arc]], dtype=np.int32),
            ))
        )

    hole_top_rings: list[np.ndarray] = []
    hole_bot_rings: list[np.ndarray] = []
    for k in range(k_holes):
        psi_k = 2.0 * math.pi * float(k) / float(k_holes)
        cx_k = r_hole_ring * math.cos(psi_k)
        cy_k = r_hole_ring * math.sin(psi_k)
        ht = mb.add_circle_ring(cx_k, cy_k, r_h, z_top_h, m_hole, phase_rad=psi_k)
        hb = mb.add_circle_ring(cx_k, cy_k, r_h, z_bot_h, m_hole, phase_rad=psi_k)
        mb.add_quad_strip(hb, ht, reverse=True)
        hole_top_rings.append(ht)
        hole_bot_rings.append(hb)

    # Build sector 0 local 2D template once, then map identically across all K sectors (top +Z & bottom -Z)
    verts_xy = mb.get_vertices_array()[:, :2]

    def _sector_loops(k: int, is_top: bool) -> tuple[list[int], list[int]]:
        k_next = (k + 1) % k_holes
        sp = spokes_top if is_top else spokes_bot
        in_r = in_top_ring if is_top else in_bot_ring
        out_r = out_top_ring if is_top else out_bot_ring
        h_r = hole_top_rings[k] if is_top else hole_bot_rings[k]

        outer_arc = [int(out_r[(k * s_arc + s) % m_ang]) for s in range(s_arc)]
        inner_arc = [int(in_r[(k * s_arc + s) % m_ang]) for s in range(s_arc, 0, -1)]
        cell_loop = [
            *sp[k][:-1].tolist(),
            *outer_arc,
            *sp[k_next][::-1][:-1].tolist(),
            *inner_arc,
        ]
        return cell_loop, h_r.tolist()

    sec0_outer, sec0_hole = _sector_loops(0, True)
    local_nodes_0 = sec0_outer + sec0_hole
    local_xy_0 = verts_xy[local_nodes_0]
    n_cell = len(sec0_outer)
    n_h = len(sec0_hole)
    template_tris = _mg_triangulate_cell_2d(
        local_xy_0,
        list(range(n_cell)),
        [list(range(n_cell, n_cell + n_h))],
    )

    all_top_tris: list[np.ndarray] = []
    all_bot_tris: list[np.ndarray] = []
    for k in range(k_holes):
        ct, ht = _sector_loops(k, True)
        map_t = np.asarray(ct + ht, dtype=np.int32)
        all_top_tris.append(map_t[template_tris])

        cb, hb = _sector_loops(k, False)
        map_b = np.asarray(cb + hb, dtype=np.int32)
        tris_b = map_b[template_tris][:, [0, 2, 1]]
        all_bot_tris.append(tris_b)

    mb.add_triangles(np.vstack(all_top_tris + all_bot_tris))


def generate_gear_mesh(
    params: dict[str, Any],
    which: str = "pinion",
    resolution: str = "high",
) -> MeshData:
    """Generate a strict 2-manifold 3D gear mesh (spur, helical, or herringbone) with full body features."""
    p = normalize_params(params)
    res = "high" if str(resolution).strip().lower() == "high" else "low"
    body_key = "gear" if str(which).strip().lower() == "gear" else "pinion"
    body_cfg = p[body_key]

    geom = compute_gear_pair_geometry(p)
    g_info = geom[body_key]

    m_n = float(geom["m_n"])
    beta_deg = float(geom["beta_deg"])
    gear_type = str(p["gear_type"])
    face_w = float(p["face_width_mm"])
    pitch_r = float(g_info["pitch_radius_mm"])
    root_r = float(g_info["root_radius_mm"])
    tip_r = float(g_info["tip_radius_mm"])
    hand = str(g_info["helix_hand"])

    samples_per_flank = 12 if res == "high" else 7
    raw_chamfer = float(p["elephant_foot_chamfer_mm"])
    chamfer = min(
        max(0.0, raw_chamfer),
        0.22 * face_w,
        0.30 * m_n,
        0.24 * max(0.2, tip_r - root_r),
    )
    if chamfer < 0.03:
        chamfer = 0.0

    z_levels, insets = _mg_build_outer_z_schedule(
        face_width_mm=face_w,
        beta_deg=beta_deg,
        gear_type=gear_type,
        chamfer_mm=chamfer,
        resolution=res,
    )

    contour_std = build_gear_2d_contour(
        p,
        which=body_key,
        samples_per_flank=samples_per_flank,
        radial_inset_mm=0.0,
    )
    contour_chamf = (
        build_gear_2d_contour(
            p,
            which=body_key,
            samples_per_flank=samples_per_flank,
            radial_inset_mm=chamfer,
        )
        if chamfer > 0.0
        else contour_std
    )

    mb = _GearMeshBuilder()
    outer_rings: list[np.ndarray] = []
    outer_xy_bot: np.ndarray | None = None
    outer_xy_top: np.ndarray | None = None

    for idx_z, (zv, ins) in enumerate(zip(z_levels, insets)):
        base_xy = contour_chamf if ins > 0.0 else contour_std
        psi = helix_twist_angle_rad(zv, face_w, pitch_r, beta_deg, hand, gear_type)
        rot_xy = _mg_rotate_2d(base_xy, psi)
        if idx_z == 0:
            outer_xy_bot = rot_xy
        if idx_z == len(z_levels) - 1:
            outer_xy_top = rot_xy
        outer_rings.append(mb.add_ring_2d(rot_xy, zv))

    mb.add_tube_grid(outer_rings, reverse=False)

    assert outer_xy_bot is not None and outer_xy_top is not None
    r_outer_min = float(
        min(
            np.min(np.hypot(outer_xy_bot[:, 0], outer_xy_bot[:, 1])),
            np.min(np.hypot(outer_xy_top[:, 0], outer_xy_top[:, 1])),
        )
    )

    # Safe inner rim radius strictly inside tooth roots & chamfer
    rim_wall = max(1.2, 0.6 * m_n)
    r_safe_inner = min(root_r - rim_wall - chamfer, r_outer_min - max(0.65, 0.35 * m_n))
    r_safe_inner = max(0.55 * r_outer_min, r_safe_inner)
    r_safe_inner = min(r_safe_inner, r_outer_min - 0.25)

    # Central bore evaluation
    bore_type = str(body_cfg["bore_type"]).strip().lower()
    m_bore = 64 if res == "high" else 48
    max_bore_r = max(0.45, min(r_safe_inner - 1.0, 0.78 * r_safe_inner))
    bore_xy = (
        build_bore_2d_contour(body_cfg, max_allowed_radius_mm=max_bore_r, radial_samples=m_bore)
        if bore_type != "none"
        else None
    )

    if bore_xy is not None:
        r_bore_max = float(np.max(np.hypot(bore_xy[:, 0], bore_xy[:, 1])))
        if r_bore_max >= r_safe_inner - 0.55:
            scale_b = max(0.35, (r_safe_inner - 0.65) / max(r_bore_max, 1e-6))
            bore_xy = bore_xy * scale_b
            r_bore_max = float(np.max(np.hypot(bore_xy[:, 0], bore_xy[:, 1])))
        collar_pad = max(0.45, min(1.1, 0.28 * (r_safe_inner - r_bore_max)))
        r_collar = min(r_safe_inner - 0.25, r_bore_max + collar_pad)
    else:
        r_bore_max = 0.0
        r_collar = min(max(0.8, 0.18 * r_safe_inner), 0.45 * r_safe_inner)

    avail_span = max(0.0, r_safe_inner - r_collar)

    # Resolve concentric body features (hub, recess, web_recess, lightening_holes)
    light_mode = str(body_cfg["lightening_mode"]).strip().lower()
    k_holes = int(body_cfg["lightening_hole_count"])
    holes_active = bool(light_mode == "lightening_holes" and k_holes >= 1 and avail_span >= 1.1)
    web_active = bool(light_mode == "web_recess" and avail_span >= 1.2)

    hub_req = bool(body_cfg["hub_enabled"]) and float(body_cfg["hub_height_mm"]) > 0.08
    rec_req = bool(body_cfg["recess_enabled"]) and float(body_cfg["recess_depth_mm"]) > 0.08
    rec_side = str(body_cfg["recess_side"]).strip().lower()

    if holes_active or web_active:
        rim_step = max(0.30, min(1.0, 0.07 * avail_span))
        r_web_out = r_safe_inner - rim_step
        min_web_span = max(0.95, 0.36 * avail_span)
        r_core_limit = max(r_collar + 0.30, r_web_out - min_web_span)

        r_core_target = r_collar + max(0.35, 0.18 * avail_span)
        if hub_req:
            r_core_target = max(r_core_target, 0.5 * float(body_cfg["hub_diameter_mm"]))
        if rec_req:
            r_core_target = max(r_core_target, 0.5 * float(body_cfg["recess_diameter_mm"]))

        r_web_in = max(r_collar + 0.28, min(r_core_target + 0.35, r_core_limit))
        r_feature_cap = max(r_collar + 0.25, r_web_in - 0.28)
    else:
        r_web_in = 0.0
        r_web_out = 0.0
        r_feature_cap = r_safe_inner - 0.25

    r_hub = 0.0
    hub_h = float(body_cfg["hub_height_mm"])
    if hub_req and r_feature_cap > r_collar + 0.22:
        r_hub = max(r_collar + 0.25, min(0.5 * float(body_cfg["hub_diameter_mm"]), r_feature_cap))

    r_rec = 0.0
    rec_depth = float(body_cfg["recess_depth_mm"])
    if rec_req and r_feature_cap > r_collar + 0.22:
        r_rec = max(r_collar + 0.25, min(0.5 * float(body_cfg["recess_diameter_mm"]), r_feature_cap))
        # Avoid microscopic sub-0.25mm step if hub and recess diameters are nearly equal
        if r_hub > 0.0 and 0.0 < abs(r_rec - r_hub) < 0.25:
            r_rec = r_hub

    # Assemble strictly increasing radial knots from r_collar to r_safe_inner
    raw_knots = [r_collar, r_safe_inner]
    if r_hub > 0.0:
        raw_knots.append(r_hub)
    if r_rec > 0.0:
        raw_knots.append(r_rec)
    if holes_active or web_active:
        raw_knots.extend([r_web_in, r_web_out])

    raw_knots.sort()
    knots: list[float] = [raw_knots[0]]
    for rk in raw_knots[1:]:
        if rk - knots[-1] >= 0.20:
            knots.append(rk)
        elif rk == raw_knots[-1]:
            knots[-1] = rk

    # Ensure [r_web_in, r_web_out] remains an exact single radial interval when holes_active is True
    hole_interval_idx = -1
    if holes_active:
        # Snap closest knots to r_web_in and r_web_out and drop any interior knot strictly between them
        cleaned_knots: list[float] = []
        for rk in knots:
            if r_web_in + 0.05 < rk < r_web_out - 0.05:
                continue
            cleaned_knots.append(rk)
        knots = cleaned_knots
        for idx_k in range(len(knots) - 1):
            mid_k = 0.5 * (knots[idx_k] + knots[idx_k + 1])
            if r_web_in - 0.05 <= mid_k <= r_web_out + 0.05:
                hole_interval_idx = idx_k
                break

    n_intervals = len(knots) - 1
    z_top_intervals: list[float] = []
    z_bot_intervals: list[float] = []
    min_floor = min(1.2, 0.45 * face_w)

    for idx_i in range(n_intervals):
        r_mid = 0.5 * (knots[idx_i] + knots[idx_i + 1])
        zt = face_w
        zb = 0.0

        if r_hub > 0.0 and r_mid < r_hub - 1e-5:
            zt += hub_h

        if r_rec > 0.0 and r_mid < r_rec - 1e-5:
            avail_t = zt - zb
            if rec_side == "top":
                d = min(rec_depth, max(0.0, avail_t - min_floor))
                zt -= d
            elif rec_side == "bottom":
                d = min(rec_depth, max(0.0, avail_t - min_floor))
                zb += d
            else:
                d = min(rec_depth, max(0.0, 0.5 * (avail_t - min_floor)))
                zt -= d
                zb += d

        if web_active and (r_web_in - 1e-5) < r_mid < (r_web_out + 1e-5):
            w_t = max(min_floor, min(float(body_cfg["web_thickness_mm"]), face_w - 0.25))
            d_web = max(0.0, 0.5 * (face_w - w_t))
            if d_web > 0.06:
                zt = face_w - d_web
                zb = d_web

        z_top_intervals.append(zt)
        z_bot_intervals.append(zb)

    # Angular grid for concentric rings
    if holes_active and hole_interval_idx >= 0:
        s_arc = max(8 if res == "high" else 6, int(math.ceil((64.0 if res == "high" else 40.0) / k_holes)))
        m_ang = k_holes * s_arc
        dpsi = math.pi / float(k_holes)
        ring_thetas = -dpsi + np.linspace(0.0, 2.0 * math.pi, m_ang, endpoint=False, dtype=np.float64)
    else:
        s_arc = 0
        m_ang = 64 if res == "high" else 44
        ring_thetas = np.linspace(0.0, 2.0 * math.pi, m_ang, endpoint=False, dtype=np.float64)

    inner_top_ring = mb.add_polar_ring(knots[0], ring_thetas, z_top_intervals[0])
    inner_bot_ring = mb.add_polar_ring(knots[0], ring_thetas, z_bot_intervals[0])

    cur_top = inner_top_ring
    cur_bot = inner_bot_ring

    for idx_i in range(n_intervals):
        r_next = knots[idx_i + 1]
        zt_cur = z_top_intervals[idx_i]
        zb_cur = z_bot_intervals[idx_i]

        next_top = mb.add_polar_ring(r_next, ring_thetas, zt_cur)
        next_bot = mb.add_polar_ring(r_next, ring_thetas, zb_cur)

        if holes_active and idx_i == hole_interval_idx:
            _mg_add_k_hole_sectors(
                mb=mb,
                in_top_ring=cur_top,
                out_top_ring=next_top,
                in_bot_ring=cur_bot,
                out_bot_ring=next_bot,
                ring_thetas=ring_thetas,
                r_ann_in=knots[idx_i],
                r_ann_out=r_next,
                z_bot_h=zb_cur,
                z_top_h=zt_cur,
                k_holes=k_holes,
                s_arc=s_arc,
                req_hole_diam_mm=float(body_cfg["lightening_hole_diameter_mm"]),
                resolution=res,
            )
        else:
            mb.add_quad_strip(cur_top, next_top, reverse=True)
            mb.add_quad_strip(cur_bot, next_bot, reverse=False)

        cur_top = next_top
        cur_bot = next_bot

        # Vertical Z step to next radial interval (or back to z=face_w / z=0 at r_safe_inner)
        zt_target = z_top_intervals[idx_i + 1] if (idx_i + 1) < n_intervals else face_w
        zb_target = z_bot_intervals[idx_i + 1] if (idx_i + 1) < n_intervals else 0.0

        if abs(zt_target - zt_cur) > 1e-5:
            step_top = mb.add_polar_ring(r_next, ring_thetas, zt_target)
            mb.add_quad_strip(cur_top, step_top, reverse=True)
            cur_top = step_top

        if abs(zb_target - zb_cur) > 1e-5:
            step_bot = mb.add_polar_ring(r_next, ring_thetas, zb_target)
            mb.add_quad_strip(cur_bot, step_bot, reverse=False)
            cur_bot = step_bot

    # Close outer rim from cur_top (at r_safe_inner, z=face_w) -> outer_rings[-1]
    # and cur_bot (at r_safe_inner, z=0) -> outer_rings[0] via angle-matched tooth collar circle
    r_tooth_collar = 0.5 * (r_safe_inner + r_outer_min)
    top_tooth_angs = np.arctan2(outer_xy_top[:, 1], outer_xy_top[:, 0])
    bot_tooth_angs = np.arctan2(outer_xy_bot[:, 1], outer_xy_bot[:, 0])

    top_tc_ring = mb.add_polar_ring(r_tooth_collar, top_tooth_angs, face_w)
    bot_tc_ring = mb.add_polar_ring(r_tooth_collar, bot_tooth_angs, 0.0)

    verts_xy_now = mb.get_vertices_array()[:, :2]
    mb.add_triangles(_mg_bridge_convex_loops_up(verts_xy_now, cur_top, top_tc_ring, (0.0, 0.0)))
    mb.add_triangles(_mg_bridge_convex_loops_up(verts_xy_now, cur_bot, bot_tc_ring, (0.0, 0.0))[:, [0, 2, 1]])

    mb.add_quad_strip(top_tc_ring, outer_rings[-1], reverse=True)
    mb.add_quad_strip(bot_tc_ring, outer_rings[0], reverse=False)

    # Close inner center (central bore tunnel or solid center fan)
    zt0 = z_top_intervals[0]
    zb0 = z_bot_intervals[0]
    if bore_xy is None:
        c_top = mb.add_vertex(0.0, 0.0, zt0)
        c_bot = mb.add_vertex(0.0, 0.0, zb0)
        mb.add_disk_fan(c_top, inner_top_ring, normal_up=True)
        mb.add_disk_fan(c_bot, inner_bot_ring, normal_up=False)
    else:
        bore_top_ring = mb.add_ring_2d(bore_xy, zt0)
        bore_bot_ring = mb.add_ring_2d(bore_xy, zb0)
        mb.add_quad_strip(bore_bot_ring, bore_top_ring, reverse=True)

        # Ray-matched intermediate circle guarantees zero inversion even on sharp keyway corners
        bore_angs = np.arctan2(bore_xy[:, 1], bore_xy[:, 0])
        r_bore_mid = 0.5 * (r_bore_max + knots[0])
        if knots[0] - r_bore_max >= 0.28:
            bmid_top = mb.add_polar_ring(r_bore_mid, bore_angs, zt0)
            bmid_bot = mb.add_polar_ring(r_bore_mid, bore_angs, zb0)
            mb.add_quad_strip(bore_top_ring, bmid_top, reverse=True)
            mb.add_quad_strip(bore_bot_ring, bmid_bot, reverse=False)
            verts_xy_all = mb.get_vertices_array()[:, :2]
            mb.add_triangles(_mg_bridge_convex_loops_up(verts_xy_all, bmid_top, inner_top_ring, (0.0, 0.0)))
            mb.add_triangles(
                _mg_bridge_convex_loops_up(verts_xy_all, bmid_bot, inner_bot_ring, (0.0, 0.0))[:, [0, 2, 1]]
            )
        else:
            verts_xy_all = mb.get_vertices_array()[:, :2]
            top_b_tris = _mg_triangulate_cell_2d(verts_xy_all, inner_top_ring.tolist(), [bore_top_ring.tolist()])
            mb.add_triangles(top_b_tris)
            bot_b_tris = _mg_triangulate_cell_2d(
                verts_xy_all, inner_bot_ring.tolist(), [bore_bot_ring.tolist()]
            )[:, [0, 2, 1]]
            mb.add_triangles(bot_b_tris)

    return mb.build(center_xy=False)


# ---------------------------------------------------------------------------
# Fit-Test Kit Generators (Sectors, 2-Pin Center Jig Base, 4-Hole Bore Gauge)
# ---------------------------------------------------------------------------


def _mg_compute_fit_pin_diameter(geom: dict[str, Any]) -> float:
    """Compute test-pin hole diameter (8.0 mm nominal, scaled cleanly for tiny gears)."""
    min_root_d = 2.0 * min(
        float(geom["pinion"]["root_radius_mm"]),
        float(geom["gear"]["root_radius_mm"]),
    )
    a = float(geom["center_distance_mm"])
    if min_root_d >= 9.0 and a >= 6.8:
        return max(4.0, min(8.0, 0.45 * min_root_d))
    return max(1.6, min(8.0, 0.45 * min_root_d, 0.58 * a))


def _mg_build_sector_2d_contour(
    full_contour: np.ndarray,
    z_teeth: int,
    sector_teeth: int,
    r_hub_out: float,
) -> np.ndarray:
    """Extract a 5-tooth arc sector and close around (0, 0) via flared radial spokes & circular back hub.

    Every point on the returned CCW contour has strictly increasing polar angle around (0, 0)
    and radius >= r_hub_out, enabling analytical 2-manifold bridging at arbitrary helix twist!
    """
    n_total = len(full_contour)
    pts_per_tooth = n_total // z_teeth

    # Centered 5-tooth slice around Tooth 0 (+X): teeth [-half .. +half]
    n_left = sector_teeth // 2
    n_right = sector_teeth - n_left  # e.g. for 5 teeth: 2 before tooth 0, plus teeth 0, 1, 2
    start_idx = (z_teeth - n_left) * pts_per_tooth
    end_idx = n_right * pts_per_tooth

    arc_pts = np.vstack((full_contour[start_idx:], full_contour[:end_idx]))

    # Unwrap start and end polar angles of the 5-tooth arc
    p_first = arc_pts[0]
    p_last = arc_pts[-1]
    r_first = math.hypot(float(p_first[0]), float(p_first[1]))
    r_last = math.hypot(float(p_last[0]), float(p_last[1]))

    ang_first = math.atan2(float(p_first[1]), float(p_first[0]))  # negative (~ -5*pi/Z)
    ang_last = math.atan2(float(p_last[1]), float(p_last[0]))    # positive (~ +5*pi/Z)
    while ang_last <= ang_first:
        ang_last += 2.0 * math.pi

    back_span = (ang_first + 2.0 * math.pi) - ang_last
    spoke_flare = min(0.14, 0.16 * back_span)

    # Left spoke: inward from (r_last, ang_last) -> (r_hub_out, ang_last + spoke_flare)
    n_spoke = 6
    u_sp = np.linspace(0.0, 1.0, n_spoke + 1, dtype=np.float64)[1:]
    left_angs = ang_last + u_sp * spoke_flare
    left_rads = r_last + u_sp * (r_hub_out - r_last)
    left_spoke_xy = np.column_stack((left_rads * np.cos(left_angs), left_rads * np.sin(left_angs)))

    # Circular back hub arc from (ang_last + spoke_flare) to (ang_first + 2*pi - spoke_flare)
    hub_a0 = ang_last + spoke_flare
    hub_a1 = ang_first + 2.0 * math.pi - spoke_flare
    n_hub_arc = max(24, int(round(36.0 * (hub_a1 - hub_a0) / math.pi)))
    hub_angs = np.linspace(hub_a0, hub_a1, n_hub_arc + 1, dtype=np.float64)[1:-1]
    hub_arc_xy = np.column_stack((r_hub_out * np.cos(hub_angs), r_hub_out * np.sin(hub_angs)))

    # Right spoke: outward from (r_hub_out, hub_a1) -> just before (r_first, ang_first + 2*pi)
    u_sp_r = np.linspace(0.0, 1.0, n_spoke + 1, dtype=np.float64)[:-1]
    right_angs = hub_a1 + u_sp_r * spoke_flare
    right_rads = r_hub_out + u_sp_r * (r_first - r_hub_out)
    right_spoke_xy = np.column_stack((right_rads * np.cos(right_angs), right_rads * np.sin(right_angs)))

    return np.vstack((arc_pts, left_spoke_xy, hub_arc_xy, right_spoke_xy))


def _mg_generate_sector_mesh(
    p: dict[str, Any],
    geom: dict[str, Any],
    which: str,
    d_pin_hole: float,
    sector_h: float,
) -> MeshData:
    """Build strict 2-manifold 5-tooth gear sector (or full gear when Z <= 8) with vertical test-pin bore."""
    body_key = "gear" if which == "gear" else "pinion"
    g_info = geom[body_key]
    z_teeth = int(g_info["teeth"])
    r_pin_hole = 0.5 * d_pin_hole

    # If Z <= 8, full gear with round test-pin bore drops straight onto the 2-pin center jig
    if z_teeth <= 8:
        p_full = normalize_params(p)
        p_full["face_width_mm"] = sector_h
        p_full[body_key]["bore_type"] = "round"
        p_full[body_key]["bore_diameter_mm"] = d_pin_hole
        p_full[body_key]["bore_clearance_mm"] = 0.0
        p_full[body_key]["hub_enabled"] = False
        p_full[body_key]["recess_enabled"] = False
        p_full[body_key]["lightening_mode"] = "solid"
        return generate_gear_mesh(p_full, which=body_key, resolution="high")

    m_n = float(geom["m_n"])
    beta_deg = float(geom["beta_deg"])
    gear_type = str(p["gear_type"])
    pitch_r = float(g_info["pitch_radius_mm"])
    root_r = float(g_info["root_radius_mm"])
    tip_r = float(g_info["tip_radius_mm"])
    hand = str(g_info["helix_hand"])

    chamfer = min(
        max(0.0, float(p["elephant_foot_chamfer_mm"])),
        0.20 * sector_h,
        0.28 * m_n,
        0.22 * max(0.2, tip_r - root_r),
    )
    if chamfer < 0.03:
        chamfer = 0.0

    p_sec = dict(p)
    p_sec["face_width_mm"] = sector_h

    full_std = build_gear_2d_contour(p_sec, which=body_key, samples_per_flank=10, radial_inset_mm=0.0)
    full_chm = (
        build_gear_2d_contour(p_sec, which=body_key, samples_per_flank=10, radial_inset_mm=chamfer)
        if chamfer > 0.0
        else full_std
    )

    r_root_eff = float(np.min(np.hypot(full_chm[:, 0], full_chm[:, 1])))
    hub_wall = max(2.2, min(4.0, 0.45 * (r_root_eff - r_pin_hole)))
    r_hub_out = min(r_root_eff - 0.5, r_pin_hole + max(1.0, hub_wall))
    r_hub_out_chm = max(r_pin_hole + 0.65, r_hub_out - 0.5 * chamfer)

    sec_teeth = min(5, z_teeth)
    sec_std = _mg_build_sector_2d_contour(full_std, z_teeth, sec_teeth, r_hub_out)
    sec_chm = (
        _mg_build_sector_2d_contour(full_chm, z_teeth, sec_teeth, r_hub_out_chm)
        if chamfer > 0.0
        else sec_std
    )

    z_levels, insets = _mg_build_outer_z_schedule(
        face_width_mm=sector_h,
        beta_deg=beta_deg,
        gear_type=gear_type,
        chamfer_mm=chamfer,
        resolution="high",
    )

    mb = _GearMeshBuilder()
    outer_rings: list[np.ndarray] = []
    bot_xy: np.ndarray | None = None
    top_xy: np.ndarray | None = None

    for idx_z, (zv, ins) in enumerate(zip(z_levels, insets)):
        c_xy = sec_chm if ins > 0.0 else sec_std
        psi = helix_twist_angle_rad(zv, sector_h, pitch_r, beta_deg, hand, gear_type)
        r_xy = _mg_rotate_2d(c_xy, psi)
        if idx_z == 0:
            bot_xy = r_xy
        if idx_z == len(z_levels) - 1:
            top_xy = r_xy
        outer_rings.append(mb.add_ring_2d(r_xy, zv))

    mb.add_tube_grid(outer_rings, reverse=False)
    assert bot_xy is not None and top_xy is not None

    # Central vertical pin hole + ray-matched collar ring for twist-proof positive triangles
    m_pin = 48
    pin_bot = mb.add_circle_ring(0.0, 0.0, r_pin_hole, 0.0, m_pin)
    pin_top = mb.add_circle_ring(0.0, 0.0, r_pin_hole, sector_h, m_pin)
    mb.add_quad_strip(pin_bot, pin_top, reverse=True)

    r_min_outer = float(
        min(
            np.min(np.hypot(bot_xy[:, 0], bot_xy[:, 1])),
            np.min(np.hypot(top_xy[:, 0], top_xy[:, 1])),
        )
    )
    r_collar = 0.5 * (r_pin_hole + r_min_outer)
    bot_angs = np.arctan2(bot_xy[:, 1], bot_xy[:, 0])
    top_angs = np.arctan2(top_xy[:, 1], top_xy[:, 0])

    col_bot = mb.add_polar_ring(r_collar, bot_angs, 0.0)
    col_top = mb.add_polar_ring(r_collar, top_angs, sector_h)

    verts_xy = mb.get_vertices_array()[:, :2]
    mb.add_triangles(_mg_bridge_convex_loops_up(verts_xy, pin_top, col_top, (0.0, 0.0)))
    mb.add_triangles(_mg_bridge_convex_loops_up(verts_xy, pin_bot, col_bot, (0.0, 0.0))[:, [0, 2, 1]])

    mb.add_quad_strip(col_top, outer_rings[-1], reverse=True)
    mb.add_quad_strip(col_bot, outer_rings[0], reverse=False)

    return mb.build(center_xy=True)


def _mg_generate_center_jig_base(
    geom: dict[str, Any],
    d_pin_hole: float,
    sector_h: float,
) -> MeshData:
    """Build strict 2-manifold rounded-rectangle base plate with two integral slip-fit pins (genus == 0)."""
    a = float(geom["center_distance_mm"])
    slip_clearance = min(0.22, 0.08 * d_pin_hole)
    r_pin = max(0.6, 0.5 * (d_pin_hole - slip_clearance))

    z_plate = 3.0
    pin_h = sector_h + 1.5
    z_pin_top = z_plate + pin_h
    pin_chamfer = min(0.6, 0.30 * r_pin, 0.25 * pin_h)

    r_pad = max(r_pin + 4.2, 8.0)
    hx = 0.5 * a + r_pad
    hy = r_pad
    rc = min(5.5, 0.45 * hy)

    # Half-perimeters split cleanly at x == 0 so left & right pin cells are 100% convex D-regions
    n_corner = 8
    n_horiz = 6
    n_vert = 5

    # Right half CCW from (0, -hy) -> (+hx, -hy) -> (+hx, +hy) -> (0, +hy)
    rx_bot_edge = np.linspace(0.0, hx - rc, n_horiz + 1, dtype=np.float64)[1:-1]
    right_pts_list: list[tuple[float, float]] = [(float(x), -hy) for x in rx_bot_edge]

    ang_br = np.linspace(-0.5 * math.pi, 0.0, n_corner, dtype=np.float64)
    for ang in ang_br:
        right_pts_list.append((hx - rc + rc * math.cos(ang), -hy + rc + rc * math.sin(ang)))

    ry_side = np.linspace(-hy + rc, hy - rc, n_vert + 1, dtype=np.float64)[1:-1]
    for y in ry_side:
        right_pts_list.append((hx, float(y)))

    ang_tr = np.linspace(0.0, 0.5 * math.pi, n_corner, dtype=np.float64)
    for ang in ang_tr:
        right_pts_list.append((hx - rc + rc * math.cos(ang), hy - rc + rc * math.sin(ang)))

    rx_top_edge = np.linspace(hx - rc, 0.0, n_horiz + 1, dtype=np.float64)[1:-1]
    for x in rx_top_edge:
        right_pts_list.append((float(x), hy))

    right_xy = np.asarray(right_pts_list, dtype=np.float64)
    # Left half is exact 180-degree rotation (-x, -y) of right_xy
    left_xy = -right_xy

    mb = _GearMeshBuilder()

    # Plate bottom perimeter at Z = 0.0
    bot_pole_b = mb.add_vertex(0.0, -hy, 0.0)
    right_arc_b = mb.add_ring_2d(right_xy, 0.0)
    top_pole_b = mb.add_vertex(0.0, hy, 0.0)
    left_arc_b = mb.add_ring_2d(left_xy, 0.0)
    plate_bot = np.concatenate((
        np.array([bot_pole_b], dtype=np.int32),
        right_arc_b,
        np.array([top_pole_b], dtype=np.int32),
        left_arc_b,
    ))

    # Plate top perimeter at Z = z_plate
    bot_pole_t = mb.add_vertex(0.0, -hy, z_plate)
    right_arc_t = mb.add_ring_2d(right_xy, z_plate)
    top_pole_t = mb.add_vertex(0.0, hy, z_plate)
    left_arc_t = mb.add_ring_2d(left_xy, z_plate)
    plate_top = np.concatenate((
        np.array([bot_pole_t], dtype=np.int32),
        right_arc_t,
        np.array([top_pole_t], dtype=np.int32),
        left_arc_t,
    ))

    # Outer plate vertical wall & solid convex bottom fan
    mb.add_quad_strip(plate_bot, plate_top, reverse=False)
    c_bot = mb.add_vertex(0.0, 0.0, 0.0)
    mb.add_disk_fan(c_bot, plate_bot, normal_up=False)

    # Interior seam along x == 0 on top deck (from -hy to +hy)
    seam_ys = np.linspace(-hy, hy, 9, dtype=np.float64)[1:-1]
    seam_top = mb.add_ring_2d(np.column_stack((np.zeros_like(seam_ys), seam_ys)), z_plate)

    right_cell = [bot_pole_t, *right_arc_t.tolist(), top_pole_t, *seam_top[::-1].tolist()]
    left_cell = [top_pole_t, *left_arc_t.tolist(), bot_pole_t, *seam_top.tolist()]

    m_pin = 40
    pin_r_base = mb.add_circle_ring(+0.5 * a, 0.0, r_pin, z_plate, m_pin)
    pin_l_base = mb.add_circle_ring(-0.5 * a, 0.0, r_pin, z_plate, m_pin)

    verts_xy = mb.get_vertices_array()[:, :2]
    mb.add_triangles(_mg_bridge_convex_loops_up(verts_xy, pin_r_base, right_cell, (+0.5 * a, 0.0)))
    mb.add_triangles(_mg_bridge_convex_loops_up(verts_xy, pin_l_base, left_cell, (-0.5 * a, 0.0)))

    for cx, base_ring in ((+0.5 * a, pin_r_base), (-0.5 * a, pin_l_base)):
        cyl_top = mb.add_circle_ring(cx, 0.0, r_pin, z_pin_top - pin_chamfer, m_pin)
        tip_ring = mb.add_circle_ring(cx, 0.0, r_pin - pin_chamfer, z_pin_top, m_pin)
        mb.add_tube_grid([base_ring, cyl_top, tip_ring], reverse=False)
        tip_c = mb.add_vertex(cx, 0.0, z_pin_top)
        mb.add_disk_fan(tip_c, tip_ring, normal_up=True)

    return mb.build(center_xy=False)


def _mg_generate_bore_fit_gauge(p: dict[str, Any]) -> MeshData:
    """Build strict 2-manifold 4-hole bore calibration strip with 1..4 V-notch markers (genus == 4)."""
    bore_cfg = dict(p["pinion"])
    if str(bore_cfg.get("bore_type", "round")).strip().lower() == "none":
        bore_cfg["bore_type"] = "round"

    nom_d = float(bore_cfg["bore_diameter_mm"])
    if nom_d > 24.0:
        bore_cfg["bore_diameter_mm"] = 24.0
        nom_d = 24.0
    max_r = max(2.0, 0.5 * nom_d + 2.5)

    extra_clearances = (-0.05, 0.00, +0.05, +0.10)
    local_holes: list[np.ndarray] = []
    for delta_c in extra_clearances:
        hc = build_bore_2d_contour(
            bore_cfg,
            max_allowed_radius_mm=max_r,
            radial_samples=48,
            extra_clearance_mm=delta_c,
        )
        assert hc is not None
        local_holes.append(hc)

    r_hole_max = max(float(np.max(np.hypot(h[:, 0], h[:, 1]))) for h in local_holes)
    cell_w = max(2.0 * r_hole_max + 5.0, 12.0)
    hy = max(r_hole_max + 4.5, 7.5)
    z_h = 5.0

    x_splits = [-2.0 * cell_w, -1.0 * cell_w, 0.0, +1.0 * cell_w, +2.0 * cell_w]
    centers_x = [(-1.5 + float(i)) * cell_w for i in range(4)]

    # Build front (-Y) edge segments for each of the 4 cells with (i + 1) crisp V-notches
    notch_half_w = 0.55
    notch_depth = 0.85
    notch_pitch = 1.9

    front_interiors_xy: list[np.ndarray] = []
    top_interiors_xy: list[np.ndarray] = []
    for i in range(4):
        x0 = x_splits[i]
        x1 = x_splits[i + 1]
        cx = centers_x[i]
        n_notches = i + 1
        span_n = (n_notches - 1) * notch_pitch
        pts_f: list[tuple[float, float]] = []
        for idx_n in range(n_notches):
            nx = cx - 0.5 * span_n + idx_n * notch_pitch
            pts_f.append((nx - notch_half_w, -hy))
            pts_f.append((nx, -hy + notch_depth))
            pts_f.append((nx + notch_half_w, -hy))
        front_interiors_xy.append(np.asarray(pts_f, dtype=np.float64))

        tx = np.linspace(x1, x0, 6, dtype=np.float64)[1:-1]
        top_interiors_xy.append(np.column_stack((tx, np.full_like(tx, hy))))

    vert_ys = np.linspace(-hy, hy, 7, dtype=np.float64)[1:-1]

    mb = _GearMeshBuilder()

    # Vertical split lines x_splits[0..4] (from y = -hy up to y = +hy) on Z = 0 and Z = z_h
    vlines_top: list[np.ndarray] = []
    vlines_bot: list[np.ndarray] = []
    for xs in x_splits:
        col_xy = np.column_stack((
            np.full(len(vert_ys) + 2, xs, dtype=np.float64),
            np.concatenate(([-hy], vert_ys, [hy])),
        ))
        vlines_top.append(mb.add_ring_2d(col_xy, z_h))
        vlines_bot.append(mb.add_ring_2d(col_xy, 0.0))

    front_top_segs: list[np.ndarray] = []
    front_bot_segs: list[np.ndarray] = []
    back_top_segs: list[np.ndarray] = []
    back_bot_segs: list[np.ndarray] = []
    hole_top_rings: list[np.ndarray] = []
    hole_bot_rings: list[np.ndarray] = []

    for i in range(4):
        front_top_segs.append(mb.add_ring_2d(front_interiors_xy[i], z_h))
        front_bot_segs.append(mb.add_ring_2d(front_interiors_xy[i], 0.0))
        back_top_segs.append(mb.add_ring_2d(top_interiors_xy[i], z_h))
        back_bot_segs.append(mb.add_ring_2d(top_interiors_xy[i], 0.0))

        h_xy = local_holes[i].copy()
        h_xy[:, 0] += centers_x[i]
        ht = mb.add_ring_2d(h_xy, z_h)
        hb = mb.add_ring_2d(h_xy, 0.0)
        mb.add_quad_strip(hb, ht, reverse=True)
        hole_top_rings.append(ht)
        hole_bot_rings.append(hb)

    # Full CCW outer perimeter of strip (for vertical outer wall)
    def _full_strip_perimeter(is_top: bool) -> np.ndarray:
        vl = vlines_top if is_top else vlines_bot
        fs = front_top_segs if is_top else front_bot_segs
        bs = back_top_segs if is_top else back_bot_segs

        seq: list[int] = []
        # Bottom (-Y) edge from x_splits[0] -> x_splits[4]
        for i in range(4):
            seq.append(int(vl[i][0]))
            seq.extend(fs[i].tolist())
        # Right (+X) edge from -hy -> +hy (excluding top corner added next)
        seq.extend(vl[4][:-1].tolist())
        # Top (+Y) edge from x_splits[4] -> x_splits[0]
        for i in range(3, -1, -1):
            seq.append(int(vl[i + 1][-1]))
            seq.extend(bs[i].tolist())
        # Left (-X) edge from +hy -> just above -hy
        seq.extend(vl[0][::-1][:-1].tolist())
        return np.asarray(seq, dtype=np.int32)

    outer_perim_bot = _full_strip_perimeter(False)
    outer_perim_top = _full_strip_perimeter(True)
    mb.add_quad_strip(outer_perim_bot, outer_perim_top, reverse=False)

    # Triangulate each of the 4 cells on Z = z_h (+Z) and Z = 0.0 (-Z)
    verts_xy = mb.get_vertices_array()[:, :2]
    for i in range(4):
        cell_top = [
            int(vlines_top[i][0]),
            *front_top_segs[i].tolist(),
            *vlines_top[i + 1][:-1].tolist(),
            int(vlines_top[i + 1][-1]),
            *back_top_segs[i].tolist(),
            *vlines_top[i][::-1][:-1].tolist(),
        ]
        cell_bot = [
            int(vlines_bot[i][0]),
            *front_bot_segs[i].tolist(),
            *vlines_bot[i + 1][:-1].tolist(),
            int(vlines_bot[i + 1][-1]),
            *back_bot_segs[i].tolist(),
            *vlines_bot[i][::-1][:-1].tolist(),
        ]

        local_ids = cell_top + hole_top_rings[i].tolist()
        local_xy = verts_xy[local_ids]
        nc = len(cell_top)
        nh = len(hole_top_rings[i])
        local_tris = _mg_triangulate_cell_2d(
            local_xy,
            list(range(nc)),
            [list(range(nc, nc + nh))],
        )

        map_top = np.asarray(local_ids, dtype=np.int32)
        map_bot = np.asarray(cell_bot + hole_bot_rings[i].tolist(), dtype=np.int32)
        mb.add_triangles(map_top[local_tris])
        mb.add_triangles(map_bot[local_tris][:, [0, 2, 1]])

    return mb.build(center_xy=False)


def generate_fit_test_kit(params: dict[str, Any]) -> dict[str, MeshData]:
    """Generate the 4-piece 10-minute FDM Fit-Test Kit (sectors, 2-pin center jig, 4-hole bore gauge)."""
    p = normalize_params(params)
    geom = compute_gear_pair_geometry(p)
    d_pin_hole = _mg_compute_fit_pin_diameter(geom)
    sector_h = min(float(p["face_width_mm"]), 8.0)

    sector_pinion = _mg_generate_sector_mesh(p, geom, "pinion", d_pin_hole, sector_h)
    sector_gear = _mg_generate_sector_mesh(p, geom, "gear", d_pin_hole, sector_h)
    center_jig_base = _mg_generate_center_jig_base(geom, d_pin_hole, sector_h)
    bore_fit_gauge = _mg_generate_bore_fit_gauge(p)

    return {
        "sector_pinion": sector_pinion,
        "sector_gear": sector_gear,
        "center_jig_base": center_jig_base,
        "bore_fit_gauge": bore_fit_gauge,
    }


def collect_target_meshes(
    params: dict[str, Any],
    target: str | None = None,
    lang: str = "pt",
) -> list[tuple[str, MeshData]]:
    """Build localized `(name, MeshData)` export list for the requested export_target."""
    p = normalize_params(params)
    resolved_target = str(target or p.get("export_target") or "pair_separated").strip().lower()
    is_en = str(lang).strip().lower().startswith("en")

    pinion_name = "Pinion_G1" if is_en else "Pinhao_G1"
    gear_name = "Gear_G2" if is_en else "Coroa_G2"
    sec_pinion_name = "FitSector_Pinion_G1" if is_en else "SetorTeste_Pinhao_G1"
    sec_gear_name = "FitSector_Gear_G2" if is_en else "SetorTeste_Coroa_G2"
    jig_name = "CenterJig_Base" if is_en else "BaseGabarito_2Pinos"
    gauge_name = "BoreFit_Gauge" if is_en else "ReguaCalibracao_Eixo"

    if resolved_target == "pinion_only":
        return [(pinion_name, generate_gear_mesh(p, which="pinion", resolution="high"))]

    if resolved_target == "gear_only":
        return [(gear_name, generate_gear_mesh(p, which="gear", resolution="high"))]

    if resolved_target == "fit_test_kit":
        kit = generate_fit_test_kit(p)
        return [
            (sec_pinion_name, kit["sector_pinion"]),
            (sec_gear_name, kit["sector_gear"]),
            (jig_name, kit["center_jig_base"]),
            (gauge_name, kit["bore_fit_gauge"]),
        ]

    if resolved_target == "full_suite":
        geom = compute_gear_pair_geometry(p)
        d_pin_hole = _mg_compute_fit_pin_diameter(geom)
        sector_h = min(float(p["face_width_mm"]), 8.0)
        return [
            (pinion_name, generate_gear_mesh(p, which="pinion", resolution="high")),
            (gear_name, generate_gear_mesh(p, which="gear", resolution="high")),
            (jig_name, _mg_generate_center_jig_base(geom, d_pin_hole, sector_h)),
            (gauge_name, _mg_generate_bore_fit_gauge(p)),
        ]

    # Default: "pair_separated"
    return [
        (pinion_name, generate_gear_mesh(p, which="pinion", resolution="high")),
        (gear_name, generate_gear_mesh(p, which="gear", resolution="high")),
    ]

# ===========================================================================
# MODULE: gear_studio.presets_catalog
# ===========================================================================

"""Curated built-in mechanical gear presets, user preset storage, and smart printable randomizer."""

pass  # [bundled] hoisted __future__ import

import copy
import datetime as _dt
import json
import math
import random
import re
import uuid
from pathlib import Path
from typing import Any

_PRESETS_FALLBACK_GEAR_BODY: dict[str, Any] = {
    "teeth": 16,
    "bore_type": "round",
    "bore_diameter_mm": 8.0,
    "bore_clearance_mm": 0.12,
    "d_flat_depth_mm": 0.50,
    "keyway_width_mm": 2.0,
    "keyway_depth_mm": 1.0,
    "hub_enabled": False,
    "hub_diameter_mm": 14.0,
    "hub_height_mm": 5.0,
    "recess_enabled": False,
    "recess_side": "top",
    "recess_diameter_mm": 16.0,
    "recess_depth_mm": 4.0,
    "lightening_mode": "solid",
    "web_thickness_mm": 4.0,
    "lightening_hole_count": 6,
    "lightening_hole_diameter_mm": 5.0,
}

_PRESETS_FALLBACK_DEFAULT_PARAMS: dict[str, Any] = {
    "schema_version": 1,
    "name": "Par Engrenagens",
    "gear_type": "spur",
    "module_mm": 2.0,
    "pressure_angle_deg": 20.0,
    "helix_angle_deg": 30.0,
    "helix_hand": "right",
    "face_width_mm": 12.0,
    "addendum_coeff": 1.00,
    "clearance_coeff": 0.25,
    "root_fillet_coeff": 0.30,
    "tip_chamfer_coeff": 0.06,
    "auto_profile_shift": True,
    "profile_shift_g1": 0.0,
    "profile_shift_g2": 0.0,
    "backlash_mm": 0.15,
    "xy_compensation_mm": 0.02,
    "elephant_foot_chamfer_mm": 0.40,
    "center_distance_offset_mm": 0.0,
    "input_torque_nm": 1.0,
    "pinion": {
        **_PRESETS_FALLBACK_GEAR_BODY,
        "teeth": 16,
        "bore_type": "d_shaft",
        "bore_diameter_mm": 5.0,
        "bore_clearance_mm": 0.12,
        "d_flat_depth_mm": 0.50,
        "keyway_width_mm": 2.0,
        "keyway_depth_mm": 1.0,
        "hub_enabled": False,
        "hub_diameter_mm": 14.0,
        "hub_height_mm": 5.0,
        "recess_enabled": False,
        "recess_side": "top",
        "recess_diameter_mm": 16.0,
        "recess_depth_mm": 4.0,
        "lightening_mode": "solid",
        "web_thickness_mm": 4.0,
        "lightening_hole_count": 6,
        "lightening_hole_diameter_mm": 5.0,
    },
    "gear": {
        **_PRESETS_FALLBACK_GEAR_BODY,
        "teeth": 32,
        "bore_type": "round",
        "bore_diameter_mm": 8.0,
        "bore_clearance_mm": 0.12,
        "d_flat_depth_mm": 0.60,
        "keyway_width_mm": 3.0,
        "keyway_depth_mm": 1.4,
        "hub_enabled": False,
        "hub_diameter_mm": 20.0,
        "hub_height_mm": 5.0,
        "recess_enabled": False,
        "recess_side": "top",
        "recess_diameter_mm": 22.0,
        "recess_depth_mm": 3.5,
        "lightening_mode": "lightening_holes",
        "web_thickness_mm": 4.0,
        "lightening_hole_count": 6,
        "lightening_hole_diameter_mm": 8.0,
    },
    "sim_rpm": 1.0,
    "sim_direction": "cw",
    "export_target": "pair_separated",
    "auto_configure_slicer": True,
}


def _presets_clamp_float(val: Any, lo: float, hi: float, default: float) -> float:
    try:
        num = float(val)
        if not math.isfinite(num):
            return default
        return max(lo, min(hi, num))
    except (TypeError, ValueError):
        return default


def _presets_clamp_int(val: Any, lo: int, hi: int, default: int) -> int:
    try:
        num = int(round(float(val)))
        return max(lo, min(hi, num))
    except (TypeError, ValueError):
        return default


def _presets_deep_merge(dst: dict[str, Any], src: dict[str, Any]) -> None:
    for k, v in src.items():
        if isinstance(v, dict) and isinstance(dst.get(k), dict):
            _presets_deep_merge(dst[k], v)
        else:
            dst[k] = copy.deepcopy(v)


def _presets_fallback_normalize_body(
    raw_body: Any,
    default_teeth: int = 16,
    default_bore_type: str = "round",
    default_bore_mm: float = 8.0,
    default_lightening: str = "solid",
) -> dict[str, Any]:
    src = raw_body if isinstance(raw_body, dict) else {}
    bt = str(src.get("bore_type", default_bore_type)).strip().lower()
    if bt not in ("none", "round", "d_shaft", "double_d", "hex", "keyway"):
        bt = default_bore_type
    rs = str(src.get("recess_side", "top")).strip().lower()
    if rs not in ("top", "bottom", "both"):
        rs = "top"
    lm = str(src.get("lightening_mode", default_lightening)).strip().lower()
    if lm not in ("solid", "web_recess", "lightening_holes"):
        lm = default_lightening

    return {
        "teeth": _presets_clamp_int(src.get("teeth"), 6, 200, default_teeth),
        "bore_type": bt,
        "bore_diameter_mm": _presets_clamp_float(src.get("bore_diameter_mm"), 1.5, 80.0, default_bore_mm),
        "bore_clearance_mm": _presets_clamp_float(src.get("bore_clearance_mm"), -0.10, 0.80, 0.12),
        "d_flat_depth_mm": _presets_clamp_float(src.get("d_flat_depth_mm"), 0.10, 8.0, 0.50),
        "keyway_width_mm": _presets_clamp_float(src.get("keyway_width_mm"), 1.0, 20.0, 2.0),
        "keyway_depth_mm": _presets_clamp_float(src.get("keyway_depth_mm"), 0.5, 12.0, 1.0),
        "hub_enabled": bool(src.get("hub_enabled", False)),
        "hub_diameter_mm": _presets_clamp_float(src.get("hub_diameter_mm"), 4.0, 160.0, 16.0),
        "hub_height_mm": _presets_clamp_float(src.get("hub_height_mm"), 0.5, 60.0, 5.0),
        "recess_enabled": bool(src.get("recess_enabled", False)),
        "recess_side": rs,
        "recess_diameter_mm": _presets_clamp_float(src.get("recess_diameter_mm"), 4.0, 160.0, 20.0),
        "recess_depth_mm": _presets_clamp_float(src.get("recess_depth_mm"), 0.5, 60.0, 3.5),
        "lightening_mode": lm,
        "web_thickness_mm": _presets_clamp_float(src.get("web_thickness_mm"), 1.2, 60.0, 4.0),
        "lightening_hole_count": _presets_clamp_int(src.get("lightening_hole_count"), 3, 12, 6),
        "lightening_hole_diameter_mm": _presets_clamp_float(
            src.get("lightening_hole_diameter_mm"), 2.0, 60.0, 6.0
        ),
    }


def _presets_fallback_normalize(raw: dict[str, Any] | None = None) -> dict[str, Any]:
    out = copy.deepcopy(_PRESETS_FALLBACK_DEFAULT_PARAMS)
    if isinstance(raw, dict):
        _presets_deep_merge(out, raw)

    out["schema_version"] = 1
    out["name"] = str(out.get("name") or "Par Engrenagens").strip()[:80] or "Par Engrenagens"

    gt = str(out.get("gear_type", "spur")).strip().lower()
    out["gear_type"] = gt if gt in ("spur", "helical", "herringbone") else "spur"

    out["module_mm"] = _presets_clamp_float(out.get("module_mm"), 0.5, 10.0, 2.0)
    out["pressure_angle_deg"] = _presets_clamp_float(out.get("pressure_angle_deg"), 14.5, 30.0, 20.0)
    out["helix_angle_deg"] = _presets_clamp_float(out.get("helix_angle_deg"), 0.0, 60.0, 30.0)

    hh = str(out.get("helix_hand", "right")).strip().lower()
    out["helix_hand"] = hh if hh in ("right", "left") else "right"

    out["face_width_mm"] = _presets_clamp_float(out.get("face_width_mm"), 2.0, 120.0, 12.0)
    out["addendum_coeff"] = _presets_clamp_float(out.get("addendum_coeff"), 0.40, 1.40, 1.00)
    out["clearance_coeff"] = _presets_clamp_float(out.get("clearance_coeff"), 0.10, 0.50, 0.25)
    out["root_fillet_coeff"] = _presets_clamp_float(out.get("root_fillet_coeff"), 0.05, 0.45, 0.30)
    out["tip_chamfer_coeff"] = _presets_clamp_float(out.get("tip_chamfer_coeff"), 0.00, 0.25, 0.06)

    out["auto_profile_shift"] = bool(out.get("auto_profile_shift", True))
    out["profile_shift_g1"] = _presets_clamp_float(out.get("profile_shift_g1"), -0.50, 0.80, 0.0)
    out["profile_shift_g2"] = _presets_clamp_float(out.get("profile_shift_g2"), -0.50, 0.80, 0.0)

    out["backlash_mm"] = _presets_clamp_float(out.get("backlash_mm"), 0.00, 1.00, 0.15)
    out["xy_compensation_mm"] = _presets_clamp_float(out.get("xy_compensation_mm"), -0.20, 0.30, 0.02)
    out["elephant_foot_chamfer_mm"] = _presets_clamp_float(out.get("elephant_foot_chamfer_mm"), 0.00, 1.50, 0.40)
    out["center_distance_offset_mm"] = _presets_clamp_float(out.get("center_distance_offset_mm"), -1.50, 3.00, 0.0)
    out["input_torque_nm"] = _presets_clamp_float(out.get("input_torque_nm"), 0.05, 50.0, 1.0)

    out["pinion"] = _presets_fallback_normalize_body(
        out.get("pinion"),
        default_teeth=16,
        default_bore_type="d_shaft",
        default_bore_mm=5.0,
        default_lightening="solid",
    )
    out["gear"] = _presets_fallback_normalize_body(
        out.get("gear"),
        default_teeth=32,
        default_bore_type="round",
        default_bore_mm=8.0,
        default_lightening="lightening_holes",
    )

    out["sim_rpm"] = _presets_clamp_float(out.get("sim_rpm"), 1.0, 10.0, 1.0)
    sd = str(out.get("sim_direction", "cw")).strip().lower()
    out["sim_direction"] = sd if sd in ("cw", "ccw") else "cw"

    et = str(out.get("export_target", "pair_separated")).strip().lower()
    if et not in ("pair_separated", "pinion_only", "gear_only", "fit_test_kit", "full_suite"):
        et = "pair_separated"
    out["export_target"] = et
    out["auto_configure_slicer"] = bool(out.get("auto_configure_slicer", True))
    return out


if "DEFAULT_PARAMS" not in globals() or "normalize_params" not in globals():
    try:
        pass  # [bundled] resolved intra-package import
    except (ImportError, KeyError, ValueError):
        DEFAULT_PARAMS = _PRESETS_FALLBACK_DEFAULT_PARAMS
        normalize_params = _presets_fallback_normalize


_USER_PRESETS_FILENAME = "user_presets.json"


def _make_preset_params(overrides: dict[str, Any]) -> dict[str, Any]:
    """Build a normalized preset parameter dictionary from clean base defaults + overrides."""
    base = copy.deepcopy(DEFAULT_PARAMS)
    base["pinion"]["hub_enabled"] = False
    base["pinion"]["recess_enabled"] = False
    base["pinion"]["lightening_mode"] = "solid"
    base["gear"]["hub_enabled"] = False
    base["gear"]["recess_enabled"] = False
    base["gear"]["lightening_mode"] = "solid"
    _presets_deep_merge(base, overrides)
    return normalize_params(base)


def _make_builtin_entry(
    preset_id: str,
    name_pt: str,
    name_en: str,
    category: str,
    desc_pt: str,
    desc_en: str,
    overrides: dict[str, Any],
) -> dict[str, Any]:
    params_override = {"name": name_pt, **overrides}
    return {
        "id": preset_id,
        "name_pt": name_pt,
        "name_en": name_en,
        "title_pt": name_pt,
        "title_en": name_en,
        "category": category,
        "desc_pt": desc_pt,
        "desc_en": desc_en,
        "description_pt": desc_pt,
        "description_en": desc_en,
        "params": _make_preset_params(params_override),
    }


BUILTIN_PRESETS: list[dict[str, Any]] = [
    _make_builtin_entry(
        preset_id="spur_classic_1_2",
        name_pt="Redutor Clássico Reto 1:2",
        name_en="Classic 1:2 Spur Reducer",
        category="standard",
        desc_pt="Par reto ISO módulo 2.0 (16:32 dentes) versátil e fácil de imprimir sem empuxo axial.",
        desc_en="Versatile ISO module 2.0 spur pair (16:32 teeth) with zero axial thrust.",
        overrides={
            "gear_type": "spur",
            "module_mm": 2.0,
            "pressure_angle_deg": 20.0,
            "face_width_mm": 12.0,
            "pinion": {
                "teeth": 16,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 5.0,
                "d_flat_depth_mm": 0.50,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 32,
                "bore_type": "round",
                "bore_diameter_mm": 8.0,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 6,
                "lightening_hole_diameter_mm": 8.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="helical_silent_45",
        name_pt="Helicoidal Silenciosa 45° Sem Suporte",
        name_en="Silent 45° Support-Free Helical",
        category="helical",
        desc_pt="Hélice a 45° auto-suportada em FDM com engrenamento progressivo ultra-silencioso (1:3).",
        desc_en="Support-free 45° helix angle for FDM with ultra-quiet progressive meshing (1:3).",
        overrides={
            "gear_type": "helical",
            "helix_angle_deg": 45.0,
            "helix_hand": "right",
            "module_mm": 1.75,
            "face_width_mm": 14.0,
            "pinion": {
                "teeth": 15,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 5.0,
                "d_flat_depth_mm": 0.50,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 45,
                "bore_type": "round",
                "bore_diameter_mm": 8.0,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 6,
                "lightening_hole_diameter_mm": 12.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="herringbone_extruder_1_4",
        name_pt="Extrusora Espinha de Peixe Alto Torque",
        name_en="High-Torque Herringbone Extruder 1:4",
        category="herringbone",
        desc_pt="Dupla hélice simétrica em V (30°, 11:44) auto-centrante com empuxo axial líquido nulo.",
        desc_en="Self-centering V-shaped double helical pair (30°, 11:44) with zero net axial thrust.",
        overrides={
            "gear_type": "herringbone",
            "helix_angle_deg": 30.0,
            "module_mm": 1.5,
            "face_width_mm": 10.0,
            "auto_profile_shift": True,
            "pinion": {
                "teeth": 11,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 5.0,
                "d_flat_depth_mm": 0.50,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 44,
                "bore_type": "hex",
                "bore_diameter_mm": 8.0,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 6,
                "lightening_hole_diameter_mm": 9.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="nema17_to_m8_1_5",
        name_pt="NEMA 17 Eixo-D 5mm -> Eixo M8 1:5",
        name_en="NEMA 17 5mm D-Shaft to M8 1:5",
        category="robotics",
        desc_pt="Redução direta 1:5 acoplando motor de passo NEMA 17 (eixo D 5mm) a varão/parafuso M8.",
        desc_en="Direct 1:5 reduction stage coupling a NEMA 17 stepper (5mm D-shaft) to an M8 shaft.",
        overrides={
            "gear_type": "helical",
            "helix_angle_deg": 25.0,
            "module_mm": 2.0,
            "face_width_mm": 12.0,
            "pinion": {
                "teeth": 12,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 5.0,
                "d_flat_depth_mm": 0.50,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 60,
                "bore_type": "round",
                "bore_diameter_mm": 8.0,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 6,
                "lightening_hole_diameter_mm": 14.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="stub_heavy_duty",
        name_pt="Dente Curto Stub Ultra-Robusto",
        name_en="Heavy-Duty Stub Tooth Reducer",
        category="industrial",
        desc_pt="Perfil stub (adendo 0.75× e filete de raiz amplo 0.38×) para máxima resistência à flexão.",
        desc_en="Short stub tooth profile (0.75× addendum, 0.38× root fillet) for maximum bending strength.",
        overrides={
            "gear_type": "spur",
            "module_mm": 2.5,
            "face_width_mm": 16.0,
            "addendum_coeff": 0.75,
            "clearance_coeff": 0.25,
            "root_fillet_coeff": 0.38,
            "input_torque_nm": 4.0,
            "pinion": {
                "teeth": 14,
                "bore_type": "double_d",
                "bore_diameter_mm": 8.0,
                "d_flat_depth_mm": 0.80,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 28,
                "bore_type": "round",
                "bore_diameter_mm": 10.0,
                "lightening_mode": "web_recess",
                "web_thickness_mm": 6.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="high_contact_smooth",
        name_pt="Alta Razão de Contato Suave",
        name_en="Smooth High-Contact-Ratio Drive",
        category="helical",
        desc_pt="Dentes alongados (adendo 1.20×) combinados com hélice de 35° para múltiplos dentes em carga.",
        desc_en="Tall addendum (1.20×) paired with a 35° helix for continuous multi-tooth load sharing.",
        overrides={
            "gear_type": "helical",
            "helix_angle_deg": 35.0,
            "module_mm": 1.5,
            "face_width_mm": 14.0,
            "addendum_coeff": 1.20,
            "clearance_coeff": 0.30,
            "pinion": {
                "teeth": 20,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 5.0,
                "d_flat_depth_mm": 0.50,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 40,
                "bore_type": "round",
                "bore_diameter_mm": 8.0,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 6,
                "lightening_hole_diameter_mm": 8.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="micro_pinion_shifted",
        name_pt="Micro Pinhão 9 Dentes Anti-Undercut",
        name_en="9-Tooth Shifted Micro Pinion",
        category="precision",
        desc_pt="Pinhão compacto de 9 dentes com correção positiva de perfil (+0.35) eliminando adelgaçamento.",
        desc_en="Compact 9-tooth pinion with positive profile shift (+0.35) eliminating root undercut.",
        overrides={
            "gear_type": "spur",
            "module_mm": 2.0,
            "face_width_mm": 12.0,
            "auto_profile_shift": True,
            "profile_shift_g1": 0.35,
            "profile_shift_g2": 0.0,
            "pinion": {
                "teeth": 9,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 4.0,
                "d_flat_depth_mm": 0.40,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 36,
                "bore_type": "round",
                "bore_diameter_mm": 8.0,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 6,
                "lightening_hole_diameter_mm": 9.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="sync_1_1_helical_45",
        name_pt="Transmissão 1:1 Helicoidal 45°",
        name_en="1:1 Synchronous 45° Helical",
        category="helical",
        desc_pt="Par síncrono 1:1 (22:22 dentes) com hélice de 45° para inversão suave de rotação entre eixos.",
        desc_en="Synchronous 1:1 pair (22:22 teeth) with 45° helix for smooth counter-rotating shafts.",
        overrides={
            "gear_type": "helical",
            "helix_angle_deg": 45.0,
            "module_mm": 2.0,
            "face_width_mm": 14.0,
            "pinion": {
                "teeth": 22,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 6.0,
                "d_flat_depth_mm": 0.60,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 5,
                "lightening_hole_diameter_mm": 7.0,
            },
            "gear": {
                "teeth": 22,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 6.0,
                "d_flat_depth_mm": 0.60,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 5,
                "lightening_hole_diameter_mm": 7.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="bearing_608_spoked",
        name_pt="Coroa c/ Alojamento Rolamento 608ZZ",
        name_en="608ZZ Bearing-Seated Gear Pair",
        category="robotics",
        desc_pt="Coroa helicoidal com rebaixo de precisão Ø22.2×7.0 mm pronto para prensar rolamento 608ZZ.",
        desc_en="Helical driven gear featuring a Ø22.2×7.0 mm pocket engineered for a standard 608ZZ bearing.",
        overrides={
            "gear_type": "helical",
            "helix_angle_deg": 20.0,
            "module_mm": 2.0,
            "face_width_mm": 10.0,
            "pinion": {
                "teeth": 15,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 5.0,
                "d_flat_depth_mm": 0.50,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 42,
                "bore_type": "round",
                "bore_diameter_mm": 8.0,
                "recess_enabled": True,
                "recess_side": "top",
                "recess_diameter_mm": 22.2,
                "recess_depth_mm": 7.0,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 6,
                "lightening_hole_diameter_mm": 9.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="robotics_compact_m125",
        name_pt="Robótica Compacta Módulo 1.25",
        name_en="Compact Robotics Module 1.25",
        category="herringbone",
        desc_pt="Transmissão espinha de peixe fina (m=1.25, 35°, 16:48) com arraste sextavado na coroa.",
        desc_en="Fine-pitch herringbone drive (m=1.25, 35°, 16:48) with hex shaft/nut drive on the gear.",
        overrides={
            "gear_type": "herringbone",
            "helix_angle_deg": 35.0,
            "module_mm": 1.25,
            "face_width_mm": 10.0,
            "pinion": {
                "teeth": 16,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 5.0,
                "d_flat_depth_mm": 0.50,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 48,
                "bore_type": "hex",
                "bore_diameter_mm": 8.0,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 6,
                "lightening_hole_diameter_mm": 8.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="industrial_keyway_m35",
        name_pt="Industrial Módulo 3.5 Chaveta DIN",
        name_en="Industrial Module 3.5 DIN Keyway",
        category="industrial",
        desc_pt="Engrenagens pesadas módulo 3.5 (14:26) com rasgos de chaveta DIN e cubos reforçados.",
        desc_en="Heavy-duty module 3.5 gears (14:26) equipped with DIN keyway bores and reinforced hubs.",
        overrides={
            "gear_type": "spur",
            "module_mm": 3.5,
            "face_width_mm": 18.0,
            "input_torque_nm": 8.0,
            "pinion": {
                "teeth": 14,
                "bore_type": "keyway",
                "bore_diameter_mm": 10.0,
                "keyway_width_mm": 3.0,
                "keyway_depth_mm": 1.4,
                "hub_enabled": True,
                "hub_diameter_mm": 22.0,
                "hub_height_mm": 6.0,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 26,
                "bore_type": "keyway",
                "bore_diameter_mm": 12.0,
                "keyway_width_mm": 4.0,
                "keyway_depth_mm": 1.8,
                "hub_enabled": True,
                "hub_diameter_mm": 28.0,
                "hub_height_mm": 6.0,
                "lightening_mode": "web_recess",
                "web_thickness_mm": 8.0,
            },
        },
    ),
    _make_builtin_entry(
        preset_id="quick_fit_calibration",
        name_pt="Calibração Rápida de Encaixe FDM",
        name_en="Quick FDM Fit Calibration Kit",
        category="calibration",
        desc_pt="Kit rápido de 10 minutos (setores 45°, base de 2 pinos na distância entre centros e régua de furo).",
        desc_en="Fast 10-minute calibration kit (45° sectors, 2-pin center-distance jig, and 4-step bore gauge).",
        overrides={
            "gear_type": "helical",
            "helix_angle_deg": 45.0,
            "module_mm": 2.0,
            "face_width_mm": 10.0,
            "export_target": "fit_test_kit",
            "pinion": {
                "teeth": 14,
                "bore_type": "d_shaft",
                "bore_diameter_mm": 5.0,
                "d_flat_depth_mm": 0.50,
                "lightening_mode": "solid",
            },
            "gear": {
                "teeth": 24,
                "bore_type": "round",
                "bore_diameter_mm": 8.0,
                "lightening_mode": "lightening_holes",
                "lightening_hole_count": 6,
                "lightening_hole_diameter_mm": 6.5,
            },
        },
    ),
]


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")
    return slug[:32] or "preset"


def _user_presets_path(presets_dir: str | Path) -> Path:
    return Path(presets_dir) / _USER_PRESETS_FILENAME


def _sanitize_user_preset_entry(entry: dict[str, Any]) -> dict[str, Any] | None:
    if not isinstance(entry, dict):
        return None
    raw_params = entry.get("params")
    if not isinstance(raw_params, dict):
        return None
    name = (
        str(entry.get("name") or entry.get("name_pt") or entry.get("title_pt") or raw_params.get("name") or "Meu Par")
        .strip()[:80]
    )
    if not name:
        name = "Meu Par"
    preset_id = str(entry.get("id") or "").strip() or f"user_{_slugify(name)}_{uuid.uuid4().hex[:6]}"
    norm_params = normalize_params(raw_params)
    norm_params["name"] = name
    now_iso = _dt.datetime.now(_dt.timezone.utc).isoformat()
    desc_pt = str(entry.get("desc_pt") or entry.get("description_pt") or "Preset mecânico salvo pelo usuário")
    desc_en = str(entry.get("desc_en") or entry.get("description_en") or "User-saved custom gear preset")
    name_pt = str(entry.get("name_pt") or entry.get("title_pt") or name)
    name_en = str(entry.get("name_en") or entry.get("title_en") or name)
    return {
        "id": preset_id,
        "name": name,
        "name_pt": name_pt,
        "name_en": name_en,
        "title_pt": name_pt,
        "title_en": name_en,
        "category": "user",
        "desc_pt": desc_pt,
        "desc_en": desc_en,
        "description_pt": desc_pt,
        "description_en": desc_en,
        "created_at": str(entry.get("created_at") or now_iso),
        "updated_at": str(entry.get("updated_at") or now_iso),
        "params": norm_params,
    }


def _write_user_presets_file(presets_dir: str | Path, presets: list[dict[str, Any]]) -> None:
    folder = Path(presets_dir)
    if not folder.exists():
        folder.mkdir(parents=True, exist_ok=True)
    target = folder / _USER_PRESETS_FILENAME
    payload = {"version": "1.0", "presets": presets}
    with open(target, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)


def load_user_presets(presets_dir: str | Path) -> list[dict[str, Any]]:
    """Load and validate user-saved presets from presets_dir/user_presets.json."""
    target = _user_presets_path(presets_dir)
    if not target.is_file():
        return []
    try:
        with open(target, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except (OSError, json.JSONDecodeError, TypeError, ValueError):
        return []

    raw_list = raw.get("presets") if isinstance(raw, dict) else raw
    if not isinstance(raw_list, list):
        return []

    cleaned: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for item in raw_list:
        sanitized = _sanitize_user_preset_entry(item)
        if sanitized is not None and sanitized["id"] not in seen_ids:
            seen_ids.add(sanitized["id"])
            cleaned.append(sanitized)
    return cleaned


def save_user_preset(
    presets_dir: str | Path,
    name: str,
    params: dict[str, Any],
    preset_id: str | None = None,
) -> list[dict[str, Any]]:
    """Save or update a user preset in presets_dir and return the updated list."""
    existing = load_user_presets(presets_dir)
    clean_name = str(name or "").strip()[:80]
    if not clean_name:
        clean_name = str((params or {}).get("name") or "Meu Par").strip()[:80] or "Meu Par"

    norm_params = normalize_params(params if isinstance(params, dict) else {})
    norm_params["name"] = clean_name
    now_iso = _dt.datetime.now(_dt.timezone.utc).isoformat()

    target_id = str(preset_id).strip() if preset_id else ""
    updated = False
    if target_id:
        for idx, item in enumerate(existing):
            if item.get("id") == target_id:
                existing[idx] = {
                    **item,
                    "id": target_id,
                    "name": clean_name,
                    "name_pt": clean_name,
                    "name_en": clean_name,
                    "title_pt": clean_name,
                    "title_en": clean_name,
                    "updated_at": now_iso,
                    "params": norm_params,
                }
                updated = True
                break

    if not updated:
        if not target_id:
            target_id = f"user_{_slugify(clean_name)}_{uuid.uuid4().hex[:8]}"
        existing.append(
            {
                "id": target_id,
                "name": clean_name,
                "name_pt": clean_name,
                "name_en": clean_name,
                "title_pt": clean_name,
                "title_en": clean_name,
                "category": "user",
                "desc_pt": "Preset mecânico salvo pelo usuário",
                "desc_en": "User-saved custom gear preset",
                "description_pt": "Preset mecânico salvo pelo usuário",
                "description_en": "User-saved custom gear preset",
                "created_at": now_iso,
                "updated_at": now_iso,
                "params": norm_params,
            }
        )

    _write_user_presets_file(presets_dir, existing)
    return existing


def delete_user_preset(presets_dir: str | Path, preset_id: str) -> list[dict[str, Any]]:
    """Delete a user preset by preset_id and return the remaining presets list."""
    target_id = str(preset_id or "").strip()
    existing = load_user_presets(presets_dir)
    remaining = [item for item in existing if item.get("id") != target_id]
    if len(remaining) != len(existing) or _user_presets_path(presets_dir).is_file():
        _write_user_presets_file(presets_dir, remaining)
    return remaining


def generate_random_printable_params(
    seed: int | None = None,
    current_params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Generate a mechanically valid, non-jamming, bed-fitting random gear pair."""
    actual_seed = int(seed) if seed is not None else random.SystemRandom().randint(1, 99999)
    rng = random.Random(actual_seed)

    base_state = normalize_params(current_params) if isinstance(current_params, dict) else copy.deepcopy(DEFAULT_PARAMS)
    params = copy.deepcopy(DEFAULT_PARAMS)

    if isinstance(current_params, dict):
        for keep_key in ("auto_configure_slicer", "export_target", "sim_rpm", "sim_direction"):
            params[keep_key] = copy.deepcopy(base_state[keep_key])

    archetypes = [
        ("Redutor Reto", "spur", [0.0]),
        ("Transmissão Helicoidal", "helical", [20.0, 25.0, 30.0, 35.0, 45.0]),
        ("Helicoidal 45° Silenciosa", "helical", [45.0]),
        ("Espinha de Peixe", "herringbone", [25.0, 30.0, 35.0, 40.0]),
    ]
    arch_label, gear_type, beta_choices = rng.choice(archetypes)
    beta_deg = rng.choice(beta_choices)
    eff_beta_rad = 0.0 if gear_type == "spur" else math.radians(beta_deg)

    module_mm = rng.choice([1.25, 1.5, 1.75, 2.0, 2.25, 2.5])
    m_t = module_mm / max(0.5, math.cos(eff_beta_rad))

    z1 = rng.randint(11, 22)
    # Constrain Z2 so combined side-by-side footprint stays comfortably within 195 mm (< 220x220 bed)
    max_z2_for_bed = max(z1, int((182.0 - 4.5 * module_mm) / m_t) - z1)
    max_z2 = min(56, max(z1 + 4, max_z2_for_bed))
    z2 = rng.randint(min(z1, max_z2), max_z2)

    face_width = round(rng.uniform(max(8.0, 4.5 * module_mm), min(22.0, 9.5 * module_mm)), 1)
    addendum_coeff = rng.choice([0.80, 0.90, 1.00, 1.00, 1.00, 1.10])
    clearance_coeff = round(rng.uniform(0.22, 0.30), 2)
    root_fillet_coeff = round(rng.uniform(0.25, 0.36), 2)

    params["gear_type"] = gear_type
    params["module_mm"] = module_mm
    params["pressure_angle_deg"] = rng.choice([20.0, 20.0, 20.0, 22.5])
    params["helix_angle_deg"] = beta_deg if gear_type != "spur" else 30.0
    params["helix_hand"] = rng.choice(["right", "left"])
    params["face_width_mm"] = face_width
    params["addendum_coeff"] = addendum_coeff
    params["clearance_coeff"] = clearance_coeff
    params["root_fillet_coeff"] = root_fillet_coeff
    params["tip_chamfer_coeff"] = round(rng.uniform(0.04, 0.09), 2)
    params["auto_profile_shift"] = True
    params["profile_shift_g1"] = 0.0
    params["profile_shift_g2"] = 0.0
    params["backlash_mm"] = round(rng.uniform(0.12, 0.20), 2)
    params["xy_compensation_mm"] = 0.02
    params["elephant_foot_chamfer_mm"] = 0.40
    params["center_distance_offset_mm"] = 0.0

    r_root_1 = 0.5 * m_t * z1 - module_mm * (addendum_coeff + clearance_coeff)
    r_root_2 = 0.5 * m_t * z2 - module_mm * (addendum_coeff + clearance_coeff)

    pinion_bore_mm = 5.0 if r_root_1 >= 6.5 else 4.0
    gear_bore_mm = rng.choice([6.0, 8.0, 10.0]) if r_root_2 >= 12.0 else 5.0

    params["pinion"] = {
        **params["pinion"],
        "teeth": z1,
        "bore_type": rng.choice(["d_shaft", "round", "double_d"]),
        "bore_diameter_mm": pinion_bore_mm,
        "d_flat_depth_mm": 0.50,
        "hub_enabled": rng.choice([False, False, True]) if r_root_1 >= 10.0 else False,
        "hub_diameter_mm": round(min(2.0 * r_root_1 - 3.0, pinion_bore_mm + 8.0), 1),
        "hub_height_mm": 4.5,
        "recess_enabled": False,
        "lightening_mode": "solid",
    }

    gear_lightening = "solid"
    hole_diam = 6.0
    if r_root_2 >= 20.0:
        gear_lightening = rng.choice(["lightening_holes", "web_recess", "solid"])
        ann_span = (r_root_2 - 3.0) - (0.5 * gear_bore_mm + 3.0)
        hole_diam = round(max(4.0, min(12.0, 0.48 * ann_span)), 1)

    params["gear"] = {
        **params["gear"],
        "teeth": z2,
        "bore_type": rng.choice(["round", "hex", "d_shaft", "keyway"]),
        "bore_diameter_mm": gear_bore_mm,
        "d_flat_depth_mm": 0.60,
        "keyway_width_mm": 3.0,
        "keyway_depth_mm": 1.2,
        "hub_enabled": False,
        "recess_enabled": False,
        "lightening_mode": gear_lightening,
        "web_thickness_mm": round(max(3.0, 0.38 * face_width), 1),
        "lightening_hole_count": rng.choice([5, 6, 8]),
        "lightening_hole_diameter_mm": hole_diam,
    }

    params["name"] = f"{arch_label} {z1}:{z2} #{actual_seed % 10000:04d}"
    return normalize_params(params)

# ===========================================================================
# MODULE: gear_studio.exporters
# ===========================================================================

"""Binary STL and OrcaSlicer 2.5.1+ multi-object 3MF project exporters for Orca Gear Studio."""

pass  # [bundled] hoisted __future__ import

import datetime as _dt
import json
import math
import re
import struct
import uuid
import zipfile
from pathlib import Path
from typing import Any
from xml.sax.saxutils import escape as _xml_escape

import numpy as np

_STL_RECORD_DTYPE = np.dtype(
    [
        ("normal", "<f4", (3,)),
        ("v0", "<f4", (3,)),
        ("v1", "<f4", (3,)),
        ("v2", "<f4", (3,)),
        ("attr", "<u2"),
    ]
)

_CONTENT_TYPES_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
 <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
 <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>
 <Default Extension="config" ContentType="text/xml"/>
 <Default Extension="png" ContentType="image/png"/>
 <Default Extension="json" ContentType="application/json"/>
</Types>
"""

_RELS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Target="/3D/3dmodel.model" Id="rel-1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel"/>
</Relationships>
"""


def _extract_mesh_arrays(mesh: Any) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Extract validated (vertices, triangles, face_normals) arrays from duck-typed MeshData."""
    vertices = np.asarray(mesh.vertices, dtype=np.float32)
    if vertices.ndim != 2 or vertices.shape[1] != 3:
        raise ValueError(f"Expected vertices shape (V, 3), got {vertices.shape!r}")
    vertices = np.nan_to_num(vertices, nan=0.0, posinf=0.0, neginf=0.0).astype(np.float32, copy=False)

    triangles = np.asarray(mesh.triangles, dtype=np.int32)
    if triangles.size == 0:
        triangles = np.zeros((0, 3), dtype=np.int32)
    elif triangles.ndim != 2 or triangles.shape[1] != 3:
        raise ValueError(f"Expected triangles shape (F, 3), got {triangles.shape!r}")

    num_tris = triangles.shape[0]
    raw_normals = getattr(mesh, "face_normals", None)
    if (
        raw_normals is not None
        and np.asarray(raw_normals).shape == (num_tris, 3)
        and np.all(np.isfinite(raw_normals))
    ):
        normals = np.asarray(raw_normals, dtype=np.float32)
    elif num_tris > 0:
        tris_xyz = vertices[triangles]
        e1 = tris_xyz[:, 1, :] - tris_xyz[:, 0, :]
        e2 = tris_xyz[:, 2, :] - tris_xyz[:, 0, :]
        cross = np.cross(e1, e2)
        lengths = np.linalg.norm(cross, axis=1, keepdims=True)
        safe_lengths = np.where(lengths > 1e-12, lengths, 1.0)
        normals = (cross / safe_lengths).astype(np.float32)
        normals = np.where(lengths > 1e-12, normals, np.array([[0.0, 0.0, 1.0]], dtype=np.float32))
    else:
        normals = np.zeros((0, 3), dtype=np.float32)

    return vertices, triangles, normals


def _mesh_xy_extents(mesh: Any, vertices: np.ndarray | None = None) -> tuple[float, float]:
    """Return (width_x_mm, depth_y_mm) of a mesh from vertices or bounds_mm."""
    verts = vertices if vertices is not None else np.asarray(getattr(mesh, "vertices", []), dtype=np.float32)
    if verts.ndim == 2 and verts.shape[0] > 0 and verts.shape[1] >= 2:
        dx = float(np.max(verts[:, 0]) - np.min(verts[:, 0]))
        dy = float(np.max(verts[:, 1]) - np.min(verts[:, 1]))
        return max(dx, 1.0), max(dy, 1.0)
    bounds = getattr(mesh, "bounds_mm", None)
    if isinstance(bounds, dict):
        size = bounds.get("size")
        if isinstance(size, (list, tuple)) and len(size) >= 2:
            return max(float(size[0]), 1.0), max(float(size[1]), 1.0)
        bmin = bounds.get("min")
        bmax = bounds.get("max")
        if isinstance(bmin, (list, tuple)) and isinstance(bmax, (list, tuple)) and len(bmin) >= 2 and len(bmax) >= 2:
            return max(float(bmax[0]) - float(bmin[0]), 1.0), max(float(bmax[1]) - float(bmin[1]), 1.0)
    return 10.0, 10.0


def _mesh_xy_center_offset(mesh: Any, vertices: np.ndarray | None = None) -> tuple[float, float]:
    """Return the local XY bounding-box midpoint `(mid_x, mid_y)` of `mesh`."""
    verts = vertices if vertices is not None else np.asarray(mesh.vertices, dtype=np.float32)
    if verts.shape[0] == 0:
        return 0.0, 0.0
    mx = 0.5 * float(np.max(verts[:, 0]) + np.min(verts[:, 0]))
    my = 0.5 * float(np.max(verts[:, 1]) + np.min(verts[:, 1]))
    return mx, my


def _resolve_bed_dimensions(host_config: dict[str, Any] | None) -> tuple[float, float]:
    """Extract (bed_x, bed_y) in mm from host_config with 220x220 fallback."""
    bed_x = 220.0
    bed_y = 220.0
    if isinstance(host_config, dict):
        if "bed_x" in host_config:
            try:
                bed_x = max(float(host_config["bed_x"]), 60.0)
            except (TypeError, ValueError):
                pass
        if "bed_y" in host_config:
            try:
                bed_y = max(float(host_config["bed_y"]), 60.0)
            except (TypeError, ValueError):
                pass
        printer = host_config.get("printer")
        if isinstance(printer, dict):
            if "bed_x" in printer and "bed_x" not in host_config:
                try:
                    bed_x = max(float(printer["bed_x"]), 60.0)
                except (TypeError, ValueError):
                    pass
            if "bed_y" in printer and "bed_y" not in host_config:
                try:
                    bed_y = max(float(printer["bed_y"]), 60.0)
                except (TypeError, ValueError):
                    pass
    return bed_x, bed_y


def _resolve_line_width(host_config: dict[str, Any] | None) -> float:
    """Resolve active outer wall line width in mm from host_config (default 0.42 mm)."""
    if isinstance(host_config, dict):
        for direct_key in ("line_width_mm",):
            if direct_key in host_config:
                try:
                    lw = float(host_config[direct_key])
                    if 0.18 <= lw <= 2.5:
                        return lw
                except (TypeError, ValueError):
                    pass
        printer = host_config.get("printer")
        if isinstance(printer, dict) and "line_width_mm" in printer:
            try:
                lw = float(printer["line_width_mm"])
                if 0.18 <= lw <= 2.5:
                    return lw
            except (TypeError, ValueError):
                pass
        ps = host_config.get("project_settings")
        if isinstance(ps, dict):
            raw_lw = ps.get("outer_wall_line_width") or ps.get("line_width")
            if isinstance(raw_lw, (list, tuple)) and raw_lw:
                raw_lw = raw_lw[0]
            if raw_lw is not None:
                s = str(raw_lw).strip()
                if not s.endswith("%"):
                    m = re.search(r"[-+]?\d*\.?\d+", s)
                    if m:
                        try:
                            lw = float(m.group(0))
                            if 0.18 <= lw <= 2.5:
                                return lw
                        except ValueError:
                            pass
    return 0.42


def _positions_overlap(
    positions: list[tuple[float, float, float]],
    extents: list[tuple[float, float]],
    min_clearance_mm: float = 3.0,
) -> bool:
    """Return True if any two axis-aligned bounding boxes overlap on the XY build plate."""
    n = len(positions)
    for i in range(n):
        xi, yi, _ = positions[i]
        wxi, wyi = extents[i]
        for j in range(i + 1, n):
            xj, yj, _ = positions[j]
            wxj, wyj = extents[j]
            overlap_x = abs(xi - xj) < (0.5 * (wxi + wxj) + min_clearance_mm)
            overlap_y = abs(yi - yj) < (0.5 * (wyi + wyj) + min_clearance_mm)
            if overlap_x and overlap_y:
                return True
    return False


def _pack_shelves(
    ordered_indices: list[int],
    extents: list[tuple[float, float]],
    max_row_width: float,
    gap_mm: float,
) -> tuple[list[list[int]], float, float]:
    """Pack `ordered_indices` greedily into horizontal shelves bounded by `max_row_width`."""
    rows: list[list[int]] = []
    cur_row: list[int] = []
    cur_w = 0.0

    for idx in ordered_indices:
        w, _ = extents[idx]
        needed_w = w if not cur_row else (cur_w + gap_mm + w)
        if cur_row and needed_w > max_row_width:
            rows.append(cur_row)
            cur_row = [idx]
            cur_w = w
        else:
            cur_row.append(idx)
            cur_w = needed_w
    if cur_row:
        rows.append(cur_row)

    total_w = 0.0
    total_h = 0.0
    for r_idx, row in enumerate(rows):
        rw = sum(extents[i][0] for i in row) + gap_mm * (len(row) - 1)
        rh = max(extents[i][1] for i in row)
        total_w = max(total_w, rw)
        total_h += rh + (gap_mm if r_idx > 0 else 0.0)

    return rows, total_w, total_h


def _arrange_items_on_bed(
    extents: list[tuple[float, float]],
    z_offsets: list[float],
    bed_x: float,
    bed_y: float,
    gap_mm: float = 8.0,
) -> list[tuple[float, float, float]]:
    """Arrange 1 to 6+ items in a compact 2D multi-row shelf/grid layout centered on `(bed_x/2, bed_y/2)`."""
    cx = bed_x * 0.5
    cy = bed_y * 0.5
    count = len(extents)
    if count == 0:
        return []
    if count == 1:
        return [(cx, cy, z_offsets[0])]

    usable_x = max(bed_x - 8.0, 40.0)
    usable_y = max(bed_y - 8.0, 40.0)

    if count == 2:
        (w0, d0), (w1, d1) = extents
        total_w = w0 + gap_mm + w1
        if total_w <= usable_x:
            left_edge = cx - 0.5 * total_w
            x0 = left_edge + 0.5 * w0
            x1 = left_edge + w0 + gap_mm + 0.5 * w1
            return [(x0, cy, z_offsets[0]), (x1, cy, z_offsets[1])]

        total_h = d0 + gap_mm + d1
        if total_h <= usable_y and max(w0, w1) <= usable_x:
            bot_edge = cy - 0.5 * total_h
            y0 = bot_edge + 0.5 * d0
            y1 = bot_edge + d0 + gap_mm + 0.5 * d1
            return [(cx, y0, z_offsets[0]), (cx, y1, z_offsets[1])]

        # Place along bed diagonal with guaranteed AABB clearance when side-by-side exceeds bed width
        sep_x = 0.5 * (w0 + w1) + gap_mm
        sep_y = 0.5 * (d0 + d1) + gap_mm
        dx = min(sep_x, max(0.5 * sep_x + 1.0, usable_x - 0.5 * (w0 + w1)))
        dy = sep_y if dx < sep_x else 0.0
        return [(cx - 0.5 * dx, cy - 0.5 * dy, z_offsets[0]), (cx + 0.5 * dx, cy + 0.5 * dy, z_offsets[1])]

    # Multi-item 2D shelf bin-packing for 3..N items (e.g. 4-item fit_test_kit or full_suite)
    sum_w = sum(w for w, _ in extents) + gap_mm * (count - 1)
    max_single_w = max(w for w, _ in extents)

    # Evaluate both natural order and height-sorted order across candidate shelf widths
    orderings = [
        list(range(count)),
        sorted(range(count), key=lambda i: (-extents[i][1], -extents[i][0], i)),
    ]
    candidate_widths = sorted(
        {
            max(max_single_w, usable_x),
            max(max_single_w, 0.88 * usable_x),
            max(max_single_w, 0.74 * usable_x),
            max(max_single_w, 0.60 * usable_x),
            max(max_single_w, 0.52 * sum_w),
            max(max_single_w, sum_w + 1.0),
        }
    )

    best_rows: list[list[int]] | None = None
    best_total_h = 0.0
    best_score: tuple[int, float, float] | None = None

    for order in orderings:
        for cap_w in candidate_widths:
            rows, tw, th = _pack_shelves(order, extents, cap_w, gap_mm)
            fits = 0 if (tw <= usable_x and th <= usable_y) else 1
            norm_aspect = max(tw / usable_x, th / usable_y)
            area_box = tw * th
            score = (fits, round(norm_aspect, 4), round(area_box, 2))
            if best_score is None or score < best_score:
                best_score = score
                best_rows = rows
                best_total_h = th

    assert best_rows is not None
    placed: list[tuple[float, float, float]] = [(cx, cy, 0.0)] * count
    y_cursor = cy - 0.5 * best_total_h

    for row in best_rows:
        row_w = sum(extents[i][0] for i in row) + gap_mm * (len(row) - 1)
        row_h = max(extents[i][1] for i in row)
        row_cy = y_cursor + 0.5 * row_h
        x_cursor = cx - 0.5 * row_w
        for orig_idx in row:
            w_i, _ = extents[orig_idx]
            px = x_cursor + 0.5 * w_i
            placed[orig_idx] = (px, row_cy, z_offsets[orig_idx])
            x_cursor += w_i + gap_mm
        y_cursor += row_h + gap_mm

    return placed


def _build_project_settings_dict(params: dict[str, Any] | None, host_config: dict[str, Any] | None) -> dict[str, Any]:
    """Merge host project settings with structural mechanical gear overrides for OrcaSlicer 2.5.1+."""
    merged: dict[str, Any] = {}
    if isinstance(host_config, dict):
        raw_ps = host_config.get("project_settings")
        if isinstance(raw_ps, dict):
            merged.update(raw_ps)

    p = params if isinstance(params, dict) else {}

    # Gears are structural mechanical components: NEVER slice in spiral vase mode!
    merged["spiral_mode"] = "0"
    merged["spiral_mode_smooth"] = "0"

    if bool(p.get("auto_configure_slicer", True)):
        module_mm = max(0.5, float(p.get("module_mm", 2.0)))
        line_width = max(0.20, _resolve_line_width(host_config))
        wall_loops = max(4, min(6, int(round((1.8 * module_mm) / (2.0 * line_width)))))

        merged["wall_loops"] = str(wall_loops)
        merged["top_shell_layers"] = "5"
        merged["bottom_shell_layers"] = "5"
        merged["sparse_infill_density"] = "35%"
        merged["sparse_infill_pattern"] = "gyroid"
        merged["elefant_foot_compensation"] = "0.15"

    return merged


def write_binary_stl(path: str | Path, mesh: Any, header_name: str = "OrcaGearStudio") -> Path:
    """Write a duck-typed MeshData object to a standard little-endian binary STL file.

    Binary layout: 80-byte ASCII header + uint32 triangle count + F * 50-byte facet records.
    """
    out_path = Path(path)
    if not out_path.parent.exists():
        out_path.parent.mkdir(parents=True, exist_ok=True)

    vertices, triangles, normals = _extract_mesh_arrays(mesh)
    num_triangles = int(triangles.shape[0])

    clean_header = str(header_name or "OrcaGearStudio").strip() or "OrcaGearStudio"
    if clean_header.lower().startswith("solid"):
        clean_header = f"Orca_{clean_header}"
    header_text = f"{clean_header} - Orca Gear Studio Binary STL"
    header_bytes = header_text.encode("ascii", errors="replace")[:80].ljust(80, b"\x00")

    records = np.zeros(num_triangles, dtype=_STL_RECORD_DTYPE)
    if num_triangles > 0:
        tris_xyz = vertices[triangles]
        records["normal"] = normals.astype("<f4", copy=False)
        records["v0"] = tris_xyz[:, 0, :].astype("<f4", copy=False)
        records["v1"] = tris_xyz[:, 1, :].astype("<f4", copy=False)
        records["v2"] = tris_xyz[:, 2, :].astype("<f4", copy=False)
        records["attr"] = 0

    with open(out_path, "wb") as fh:
        fh.write(header_bytes)
        fh.write(struct.pack("<I", num_triangles))
        if num_triangles > 0:
            fh.write(records.tobytes())

    return out_path


def write_orca_3mf(
    path: str | Path,
    items: list[tuple[str, Any] | tuple[str, Any, tuple[float, float, float] | None]],
    params: dict[str, Any],
    host_config: dict[str, Any] | None = None,
) -> Path:
    """Write an OrcaSlicer 2.5.1+ compatible .3mf project archive with multi-object layout & slicer settings."""
    if not items:
        raise ValueError("write_orca_3mf requires at least one item in 'items'.")

    out_path = Path(path)
    if not out_path.parent.exists():
        out_path.parent.mkdir(parents=True, exist_ok=True)

    bed_x, bed_y = _resolve_bed_dimensions(host_config)
    cx, cy = bed_x * 0.5, bed_y * 0.5

    parsed_items: list[tuple[str, np.ndarray, np.ndarray, tuple[float, float], tuple[float, float]]] = []
    raw_positions: list[tuple[float, float, float] | None] = []
    z_offsets: list[float] = []

    for idx, entry in enumerate(items):
        if len(entry) == 2:
            raw_name, mesh = entry  # type: ignore[misc]
            raw_pos = None
        elif len(entry) >= 3:
            raw_name, mesh, raw_pos = entry[0], entry[1], entry[2]
        else:
            raise ValueError(f"Invalid item tuple at index {idx}: {entry!r}")

        item_name = str(raw_name or f"Gear_{idx + 1}").strip() or f"Gear_{idx + 1}"
        vertices, triangles, _ = _extract_mesh_arrays(mesh)
        ext = _mesh_xy_extents(mesh, vertices)
        local_mid = _mesh_xy_center_offset(mesh, vertices)
        parsed_items.append((item_name, vertices, triangles, ext, local_mid))

        if raw_pos is None:
            raw_positions.append(None)
            z_offsets.append(0.0)
        else:
            px, py, pz = float(raw_pos[0]), float(raw_pos[1]), float(raw_pos[2])
            raw_positions.append((px, py, pz))
            z_offsets.append(pz)

    extents_list = [it[3] for it in parsed_items]
    if any(pos is None for pos in raw_positions):
        if len(parsed_items) == 1:
            box_centers = [(cx, cy, z_offsets[0])]
        else:
            box_centers = _arrange_items_on_bed(extents_list, z_offsets, bed_x, bed_y, gap_mm=8.0)
        # Subtract local mesh midpoint so even asymmetric sector/gauge meshes land centered on their box!
        final_positions = [
            (bx - parsed_items[i][4][0], by - parsed_items[i][4][1], bz)
            for i, (bx, by, bz) in enumerate(box_centers)
        ]
    else:
        concrete_centers = [
            (pos[0] + parsed_items[i][4][0], pos[1] + parsed_items[i][4][1], pos[2])
            for i, pos in enumerate(raw_positions)
            if pos is not None
        ]
        if len(concrete_centers) >= 2 and _positions_overlap(concrete_centers, extents_list, min_clearance_mm=3.0):
            box_centers = _arrange_items_on_bed(extents_list, z_offsets, bed_x, bed_y, gap_mm=8.0)
            final_positions = [
                (bx - parsed_items[i][4][0], by - parsed_items[i][4][1], bz)
                for i, (bx, by, bz) in enumerate(box_centers)
            ]
        else:
            final_positions = [pos for pos in raw_positions if pos is not None]

    title = str((params or {}).get("name") or parsed_items[0][0] or "Orca Gear Studio").strip()
    escaped_title = _xml_escape(title, {'"': "&quot;"})
    today_iso = _dt.date.today().isoformat()
    ns_seed = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")
    build_uuid = str(uuid.uuid5(ns_seed, f"orca-gear-build-{title}"))

    object_blocks: list[str] = []
    build_items_xml: list[str] = []
    model_settings_objects: list[str] = []
    model_settings_instances: list[str] = []
    model_settings_assemble: list[str] = []

    for idx, (item_name, vertices, triangles, _, _) in enumerate(parsed_items):
        obj_id = idx + 1
        tx, ty, tz = final_positions[idx]
        esc_name = _xml_escape(item_name, {'"': "&quot;"})
        obj_uuid = str(uuid.uuid5(ns_seed, f"orca-gear-obj-{obj_id}-{item_name}"))
        item_uuid = str(uuid.uuid5(ns_seed, f"orca-gear-item-{obj_id}-{item_name}"))

        verts_py = vertices.tolist()
        tris_py = triangles.tolist()

        vertex_lines = "\n".join(
            f'     <vertex x="{vx:.5f}" y="{vy:.5f}" z="{vz:.5f}"/>'
            for vx, vy, vz in verts_py
        )
        triangle_lines = "\n".join(
            f'     <triangle v1="{v1}" v2="{v2}" v3="{v3}"/>'
            for v1, v2, v3 in tris_py
        )

        object_blocks.append(
            f'  <object id="{obj_id}" p:UUID="{obj_uuid}" name="{esc_name}" type="model">\n'
            f"   <mesh>\n"
            f"    <vertices>\n"
            f"{vertex_lines}\n"
            f"    </vertices>\n"
            f"    <triangles>\n"
            f"{triangle_lines}\n"
            f"    </triangles>\n"
            f"   </mesh>\n"
            f"  </object>"
        )

        transform_3x4 = f"1 0 0 0 1 0 0 0 1 {tx:.4f} {ty:.4f} {tz:.4f}"
        build_items_xml.append(
            f'  <item objectid="{obj_id}" p:UUID="{item_uuid}" transform="{transform_3x4}" printable="1"/>'
        )

        model_settings_objects.append(
            f'  <object id="{obj_id}">\n'
            f'    <metadata key="name" value="{esc_name}"/>\n'
            f'    <metadata key="extruder" value="1"/>\n'
            f'    <part id="1" subtype="normal_part">\n'
            f'      <metadata key="name" value="{esc_name}"/>\n'
            f'      <metadata key="matrix" value="1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1"/>\n'
            f'      <mesh_stat edges_fixed="0" degenerate_facets="0" facets_removed="0" facets_reversed="0" backwards_edges="0"/>\n'
            f"    </part>\n"
            f"  </object>"
        )
        model_settings_instances.append(
            f"    <model_instance>\n"
            f'      <metadata key="object_id" value="{obj_id}"/>\n'
            f'      <metadata key="instance_id" value="0"/>\n'
            f'      <metadata key="identify_id" value="{100 + obj_id}"/>\n'
            f"    </model_instance>"
        )
        model_settings_assemble.append(
            f'    <assemble_item object_id="{obj_id}" instance_id="0" transform="{transform_3x4}" offset="0 0 0"/>'
        )

    model_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<model unit="millimeter" xml:lang="en-US" '
        'xmlns="http://schemas.microsoft.com/3dmanufacturing/core/2015/02" '
        'xmlns:BambuStudio="http://schemas.bambulab.com/package/2021" '
        'xmlns:p="http://schemas.microsoft.com/3dmanufacturing/production/2015/06" '
        'requiredextensions="p">\n'
        ' <metadata name="Application">OrcaSlicer-2.5.1</metadata>\n'
        ' <metadata name="OrcaSlicer">2.5.1</metadata>\n'
        ' <metadata name="BambuStudio:3mfVersion">1</metadata>\n'
        f' <metadata name="Title">{escaped_title}</metadata>\n'
        f' <metadata name="CreationDate">{today_iso}</metadata>\n'
        " <resources>\n"
        + "\n".join(object_blocks)
        + "\n </resources>\n"
        + f' <build p:UUID="{build_uuid}">\n'
        + "\n".join(build_items_xml)
        + "\n </build>\n"
        "</model>\n"
    )

    model_settings_xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<config>\n"
        + "\n".join(model_settings_objects)
        + "\n  <plate>\n"
        '    <metadata key="plater_id" value="1"/>\n'
        '    <metadata key="plater_name" value=""/>\n'
        '    <metadata key="locked" value="false"/>\n'
        + "\n".join(model_settings_instances)
        + "\n  </plate>\n"
        "  <assemble>\n"
        + "\n".join(model_settings_assemble)
        + "\n  </assemble>\n"
        "</config>\n"
    )

    project_settings = _build_project_settings_dict(params, host_config)
    project_settings_json = json.dumps(project_settings, indent=2, ensure_ascii=False)

    with zipfile.ZipFile(out_path, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        zf.writestr("[Content_Types].xml", _CONTENT_TYPES_XML)
        zf.writestr("_rels/.rels", _RELS_XML)
        zf.writestr("3D/3dmodel.model", model_xml)
        zf.writestr("Metadata/model_settings.config", model_settings_xml)
        zf.writestr("Metadata/project_settings.config", project_settings_json)

    return out_path

# ===========================================================================
# MODULE: gear_studio.studio_ui
# ===========================================================================

"""Self-contained offline HTML5 + CSS3 + WebGL2 + 2D Tooth-Mesh Loupe Studio UI for Orca Gear Studio.

Generates the interactive 3D & 2D parametric mechanical gear design studio for both:
- `mode="page"`: Wide 3-column engineering studio tab inside OrcaSlicer (`PagesPluginCapabilityBase`)
- `mode="dock"`: Compact tabbed side-docked panel beside OrcaSlicer's 3D Plater (`UiDockPanel`)

Zero external CDN scripts, stylesheets, or web fonts are referenced so WebView2 runs 100% offline
without network permission prompts.
"""

pass  # [bundled] hoisted __future__ import

import copy
import json
from typing import Any
pass  # [bundled] resolved intra-package import

if "DEFAULT_PARAMS" not in globals():
    try:
        pass  # [bundled] resolved intra-package import
    except Exception:
        DEFAULT_PARAMS = None  # type: ignore[assignment]

if "BUILTIN_PRESETS" not in globals():
    try:
        pass  # [bundled] resolved intra-package import
    except Exception:
        BUILTIN_PRESETS = None  # type: ignore[assignment]

__all__ = ["get_studio_html"]


def _studio_ui_safe_json(payload: dict[str, Any]) -> str:
    """Serialize payload into script-safe JSON (escaping `</` and Unicode line separators)."""
    raw = json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    return (
        raw.replace("</", "<\\/")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
    )


import base64 as _gear_ui_b64, zlib as _gear_ui_zlib
_STUDIO_UI_HTML_TEMPLATE = _gear_ui_zlib.decompress(_gear_ui_b64.b85decode(b'c-ri}YmXzzks$b8zrve?X^@pkCK=4k%F3!rEh`^YDdlUD>@IZ|3fv$WOhy&SU`GV=QLS1?eTx~~VrTDg5=OIw1Lib)3#|qaR-?w=4Ca9Op!}};5B&?~C!Cr2BiubA_{gei>2PYPlB7S(&CSit&CSitAAPiUy4(8fY@ZF{(QxNGkMM&H-SNfaLc4u<a@aa-9JP-cCr{h$0_(Z4TaE|b$kTIM&-Rb^AscIZZVx_2UhJ~&zzriWeq5Nw{qk0Ut;vkBi}f#k?`jf+ae;M%aqNwu;FaHt2akK+rQh|+^kbFzV?XxYVL9r$L+^2|QssbRKOTBJr(xG+Pdzte&3M}LgGXyT{X37M_y#|>!yt%Pzw<&zyyu3m3oqH1-(jp=?p&1J$z+@TNo}Kczt(vu6DRK28)9<LsXCh~x$A~KNOjhot$Ni+Ef0cAFT}h~y;^rwo<E*UV+6EW+p6_cvh0014zP8{aqib^>D*30b!)YHZA;}2rhr3u(Q%7TeU&+ztE>*6)ymdZNt6k~o)?y*X$Ob__3O3z=6cP{i^E`i0eS27_0EPsH}<aM^2qhaknVYXr+;5hpT-{c{ekPQch<Fxo<D-*&EEa{TLQ-bhNbLwyD+GbQ?0sN4>nUdieS}hr|)j0^P`|2i+)yDS?xg${%mewM{66UbaCFX><a6WG8e!rPJ-Hc|3SC^K+n<|z5f8}Zvb_j^#?|)QS8Rks2sc|<hxrNbtC=C4UvHTJ}^Sn$mxcDOgS6Qh9hzYZZEhJ%~sjg<QkfTKe89%|CRctXgqX#K7fjV=9`miBW(o3^T0|Q!Wh>anb;4IuI@P6W|wYQ6a>W7RaR(v7lFq<IV`L)oD)N@9Nk2*H(F&+hW_~VvD<CZ?*l4+9sq9!tL&4`bR17t8A2^bUg-BrT3e%F9Bi|~t_#z*=euk-=y?EtHyB63(2cOwgJURDKKCxBLpOvxtP)M!uJ`aeZ@**C+@XIlh|^Qo>-B5>&D7NG(|`8V?Qit&_dD5B*K@tT21rg_3y?K+dtI;Yb@Qffce7XRb+e}K25@Hbr&@VX%bC5sb!cKEd-irVyH2;Cp1rjWNR)2I>;=yAHv6gBd;h`KM#dZ^2H$#czcXw0-hZ&!nLB&y_u-F2VyfmWGJCZO>l@j#*V)*td!3xwi}fGCymjguMx*-Vt!+N&u5V^d-roBCe)i<;J*ZcmjRhuejfQrWt<(IiRZGOr_lS8r!F4(E-}pF&Vn`tgfsWkp0!NVAp18dpm8nu)T$)#*eD8*U&;kjwyITEIEIjaVb|k-XeEP%SYMTxGUe6n2TF33az6gWqxF-bwpF~8PZZHf&nXZ_LvS=>%-H|`Mkp+|}NeV!ZJd`#SA#Xrxcx8oFrB18EG(!IMhF%vE$HCYmQeJtT*M2O3j$q9mP`}+VuKm6nc|D@Q_O>h;b;Dpd?7+&ekwOSW*(CjZn^mbChd>EF6dFk&bqt~>1oq0UIGBz)sfvP@`s5_Ch!if1K{!8{fe`}UrdgE(UYjnQmpaop4#ub=ft&&fOhl#1#(4ST0f^<;8YV4O47^GK(3ObvDd2E#I3$ogKbj0(0M{RSL}mO0=@CMkegGT`P^Kf|vYCttz}N1vXP_rSN1wp>-CI+w4R~s1bHD}{<FXIy4-gV*;Dwm{Y8u6U|E4T-$ZbYTN4ew0S03m23wMHTbJkEZ3V1`Ui<z^6RuO#=L7v9}$jTbjgvHD6S))$kx}+!*4MJEn#YBDsYe~<$-ewM;$(0UpTCa?aPL}E}bw;f5BY#{Lq&A=qgNs0)6^=D6<Zp{P@281@6Bt<Y0*e3&#aex%=UuEym5o*ZbX6_@G`iILJC9tFB^Xj$c+(^$5lZqGMK6pbiQg>cuP#KdAP??7%3*M|Jl*f}*((9jRwJ2iSAx9v`MRM?#Cl~zNJKA=kyn66xm=f`@@fE0Qo4sy@hWsDyeVAQILb83^CXW@Ry2NHgi$RH;Kh`JSu!R}ol`g^?6o9GflW?<8S9CZ5cdULNbvexjtHcvHfh}vQo<(0c0cG&BO*sIjge84)kKGoD?BR`U?v=liEm3de@rXaA}q0Ki4~;MgUspm;K2-GgIeg4W0yf)RPj=)acu^Jp}KJ`Wk`Kp$jB_kff`6MU{UZVksq0q>;<tdckY{F=YA$xHuxGbbG75TW~OMx=J~1tWs!fP<)^ja!7R|7czhSum?7Hq78TcQ<Z?~clw4wd&*Zgv`kpnN4W^QEt2+%N1TqPH*+XM4D+F*RuSct?*^OybqaTDLNT_Z_Gvpx-2-lIe$3a}&hH-H_L*V*+xtMJ5N_n!u*4soo$WWJFRznJ5p)wBL*!!#q<B?RB6}W^#c^}`PykB>8vH|R}JA^4E^joZ2_JM7vn!z8*;sZtayhwFAZ@o^7K)H0|-Y!|XP2w2ZaC%XGtD~~mpe&4^7%;*z1NlV|mZZYX*?fhXij@{vJOs0(Cs3BWdYf&&F!7qXOsS&FaJ>m6YvfP`KZeQ9o(JJ;nq};12!ce@#jjM(mqIwgyq9XHl<8GN;ky73B;(){1j=ZF^P<f61raVVxHpFCu;>))Td>-Iiq?lwu5WDStvoo20Dx=b%kD!`n9fo3vzn*Yho0miA)UpBW{v<BwW+jT9l<S9n^)&s#JQs&kuL*j+-V#b3yfG?mY`j-(cs*&7r=h`IOuuo#J%({TrAI8ZYLt1=|OHe#$Uz|DTVAkZ?IIqkf8+c5W?&EOSwd`EZ206n1-NTe}{$G5}CQSg~ipkYGrGNhMlqcA}CTzbge^QlVQE#3okLKP8QAjFhe((rBqk|D|`w4LleJwD9+w6z$Dm(UPkO=*7Ss~smV*Ez-%q#J#NlMy^=k@m5F27Nxmf&3$7`FGW{V8Fq=jz*4EkFs$}h^i3K&aYdV>DFhG%)y{i@q_6#mweutot@3_5-H1gGa<nyejc+z2xqazi)CAN>5(`fG8$W^hkr;OF{xijU@rar6}XRx)7*m-b869qTg`GyzbQbb~#$<1jZ(vkLGAjo95ZmorhA<Wv1Z>DV)ia)Ys>WANeC6=05i@>|cb|;##<zI4puhCt%PA{;Hnlb+junVserNxXpc?$1Y=tW)}C7SMp63Tslh~ne!oGAcw2mZv|w`tSa<UeO&{(E591-@;bduw#=TNx-ZDp47C5$1r**<Xa-#B<}Kvnux(RldI{*>)E+dZ|N+`&;JTBSU|d`o1FvTriGW@+X0ufT0IC0gaYkVm32OLYv=~Nhndp=h<^ItT(oe$CgyM+aXTUs5bMQ>&`|StpS5o=ctrgJBuu?8UrMUfzpQRm^M%OJAHid&Zi_A8st><WyV6N)<~@|n$XkA%gkNI3_JdNSz;7!z^6894=S6vx}1_*?-`ArH&naCWNO3i79>qfQ=2?L#MtV>AvxKw&fIF*b9vnq?pgcg#93s^;s0QkZKg%J=B1E#24J4Y=S=taz?c>tXHIq-?W`3caxcBIfGJP>Q#J-&z~`VW#W{_hxy`2}l%72|8hA4dIu<UKVB(Fl)CQ|)a(FjGZ@uHWUe5M-nZv#HY(+(w`MLVk^e#q7${sfZHLv`*JK#HD?_$<b_V4Am($TC!YTZUeGt58sI4mVMtTlThXGUkw``?3oDBBX0f8ru&ww&&laaLf$DPK4_pmZOv8OnSU7zKpNF7!GKhG>-8o4P~x1h=T%F4K*}dE3o=qexxt_z?<7hYxEL!A6E|N0_+HDOj7o{uyJx!N>j`nL5`YfpEQahqNPF{;+kHg%$>|JQ~^dm05<9c?K9U57Z2;*)w$3jC?oq%97H0DQircQgeJAXwb&fk*=%CLzfRFp4Y7%jg!z`-yV?q^l;h1uFWy<y-oW3?w%q9X*%}fJfmM4jh@ffBW)Je)O44=b&0>8<uSMX7G4?WKgeRbk?s3atJIfRd)`_df9G)_g1m@tCNMQ%RlD#CFDq0i;%mc~nq#RunZUZ@j=NeTS!p@0iyO<j^rTE-sV-*FXHJJSuTlD~Z9nhY&APQqslN{&9m#`^;z7-k&ve_X@$<ISZHINk7;zE09b0$NeMV~0ovEkoO|;Vmx@%Od@f#mp-)IFF7eiC)rLRkS5-zA4s8gAk8ZPtJ7O^%77p2ZH=)Ts*y1s6W^;X_WY&Dr|T@p7I4Q^EjYSd4Btg|=K{up*f`CFgGoT-;|LE4H^7;bNOJQ#Mlj*3w!6dvXxE@zKT(RJzM*-z{Nx}{+Lw9+O@F0-3m&<AO|JMg-%VS~29(qk~+pL`jR2GO$Ip?*-r^-e6Hu<Vrk9&GeO5AQkT+x={xfcL$S-A@*>Wp@Od$xe8eCNu0kumH@gJ=Tm}P{dYP(;u-GZRCP5ChztY=Inv+2;xEc*oy}22)4-{$q#i=2pYPJXNx}n7V~tG7d^7wY%V8gjJfd2^;t&k92b<@RyDmA;vj&cs@%Q0e%J*W>c+_WtiGX~yR1u9y5E;|qe}Dr%Iw9TTnx)ycYNtai(HXW6j#DB4yGW}T|sbrt>z2STdkFC-F-kS)d6->WQ~J>u6QUnq8UcT2f7TI>9%8@NG-7E(tLeked`vH3arc=XM-lHc1xjFRk&Xa-6+bRu!Ct&S<ZW5FcF7oNYQCn+!BD_tJ8z7K?oaSat*7b5Ko`RttXTJ!yl<g!h9$@&Rv|<#et=y&Vuefi=Dj)nBUG3AvWfYlr1=WI!Sl3yUr+m>SWD~?lfKw194FBz&I#y*7Me*Wlswq%tkfayfo7lBIj5opQZWo2<zbijH1Urg@r2!$zh7D{Os8$dwl7e;QY`WBj*dmY~rP^b#1+aBh*F?0TESlSo#3E{(>Gv@6G)w87S(OIDJu0HHM*Vwj+{pMz@uR`rA}Hl_0H;%I%+1g+E*TlJHjU5m)fKlnEHG?q-9g<Fgvx=cnDJQ_Y2qFtVZJ3Dpef$>E&i%sZTu)L+`eq1F%apDvw}djSY><i(-iT~3>Pt5+?*P9MN-%r<hF^)K&WxV_WiGwqEBA<Qt4!sD@6$d)w-*K^%0G7Q3*p(q@EB~x3!Jd^KSw<x1a755qy=$th*i?wU(HacasfNnhSsvUJ@DjvBLC~)D8d)Wu73#>m`GGLKI*1O(pduwA3o2ba|2v^ed2`n!J8(LS|PQ=2oW$xUwwL-^QMohzsxJ2Q1!=Mb?zUff7#H-!k$Lt74ZO<FVZre?+I{PCo$@!MX4Hw@HFG|3>`_pf}`|_D}vV(oT`;FTS?Mwo_;{|HvxrZ<~!imZFE{a(8VREg$p*IAZ>kR#?p1<lZ?eZd9LNWWk<Zu=)*>+#8=Nrz9gPx_1x{U73Ij4zYZ<09fWSl#_uk*y&UOXT0US{^83h(uM@Ttr4<Zj-Ky93zg0a1FHwyZO{nuVfmh`+U~TFTt=U~^$NxO^cq=TI!$T$OpHOT!aySPk7tBra;I5DCis&dX|nDa;~zj26W*i`)QNLOOqllZ9+K%{!ZYIb(6@@D3L(Hs?e`cm=zDcj(c=DUZIFQd~AN4yCsiKHN(*u62k1Q|f-+<j?nS+wAbLN%LgR7AJ9fmnT*ZckGW`&iO!|v*|GMFq%{Z`br;z=XpR7s5y3HFJH`N5mutw-E_8`t!!G<?gJgRRvAWHs><^+8(OxOW*DwuaR1F~@1`HRBQHw&K};A1Blcz1@f>X9tn)<tU&fvc%Dp9f0%JLloD5Jn8ksvhj7J3klNrNp!HGxAQl@i0_x?nObQjyTxTfj57vlirKv&#z@W<?&%q;x0g5TDJLgk1{*u2^P-fR);S=+~K1>#+|4!Q0!+5MfPO;D{5a|t0i-K9plGRD$}Iuo;{p62ekgqc8K`+5l%ZDk>#ns=}b)b6n6Af|p4O}(f*^rQGr{(tKkH$|Lk-c1qJBCR_4N`BS=EN*tttz*>;s{<Npveq85m(8|1B*-srMXS~GObs~}HLVd`4t<cl3mMdexBI+?bmN*g1esJG2eFqw7_)X)3;Dz?XzfWy@kkANl^6p5Rh8Ne^m%>58pNLL0F-Wz+Yk8JBup7f`7-Yo@Ow2V-07@5H=+*As4&P{;u7mKuDsHn!VE1qLkV5v>~Q(uW@dzxbY!x$r?;*}tc#9h2PSh$AL<f@sq5>$B>aGu2iD36z4JC1qWq8}>X4WA^kXlIP=~r-GONE!{2UG;FNn^@hEBIDR|YNguDMYS>Zi<2i<#Ed)j!+kqZPQYl$-=WZV+5FDRDN&n5-M16V<QpUwb|M7*O5;;$lO1|782llp(jI(+1Zb?)6~!U<sBfdzUcoQNo1gdDsH?2uHor-Gh@YY~Nlublki%ev_pIO>i@2u{6I3txohFJa}L^LOiHmUJ2i)WFU?GiXwPziQ%f2(m=g14Dv5erx!7bQgJa1I_^-H_SSZnbLZpt_#d>vc2AGb8oMplJlxwa@15>`pB<m>?X%*)CH;C7^e~J%;8*y!B`p3vo5yK|A#PvTO@Sh>hwNL;EoDb%Oj9hcW>&C8xklBb&Yo8}Gj7r{>UAFAl%trKhUJ=Z)ilqcb7_myEL1EXF~bF{UY$dsT>D^6+|XK}VxGZnb57g3%fafbQo^xhcA07JMZ_5><OE5QoFPWFIunMBMzuP#gdK4zSr}&8Am)S2&^}ZBpV|Ex@=O_mvH|cENyEnloU4(6-RhDx|AZ{!BHX~;DnlLLi<aU88z2X9r;ezqcj}2%n^vz8?9pI+?+SvB1}0$u`l0tuMB$2@&hYO9PEh7fL{947olYqjI-%|gWESr&O_o&94c+pgsQqt79zNnw)D);%l~hxzlMbnyVVy@qZ1!52A2_gDO#%lxdf-60+eKsSqc!p7%cC{%3Jpcd*Qk)ZScBS(de6q5+)%UUU$QQGzCJGKfzTm~u}2@3%dB;J#-8mr_V&+NxlF0zh{&wP6R8>$(V%MazeR3VK1T8`Fw$fm7worgR6VE}U0!fS<#C~QzaUmc{vEZ4C&BgO0-Cg)b@+b)_iw|;1sstALnqGH03LQzc=vc0l~S2n7BHPkO(o&Bx$90I7igPcB)@{)h)hqA1N4OBcNegDP}wN3?v3~oJ}%TNPGQX`J#pg!>pd<ULlIW5Y+TkVoAkX_uRNe1kcfUs1N@GO>c>W<&fwp$R;e-gcU*HSn`kxIOj7EV`&6VXQ#LE>yogM((9w`bdLr(%O@X{qsplbIyH776TvDU({Xymar9cUOZ4$z@V+Zyq>X!}*xcTxzamE_3Mn0R!h~@@IfVO0oA~q^yJeh<=wVGV@^`Q^&t*lhyf`n!%$-tj<<qG$C1r!@YZ+wAFvsDG=bB9yNJA>Bt#}~j~pgWGE0&_#(<sPYz3xvy=>xb-wnpw;5H6o?U7=@FWC?-sUyG>z-n?t_~lk<!hgHMvYdGylaSr>Lv^r4bACbZ2h>^${gr{{Os!QL_Z?LRWdsowsK|JkUr(FoJ3mG#lc1gdpZd`-y<GsblyGWZh^gbrFgVCDsiDCh|x;|VLGd;%p{aW@W!E1#DNOj=lWzWMY2>(LsAmIpla<^ezV6!6bX;Qu%mIIw6i^51x=7I4dNkJQe;{_TJIP4>u;NcU@7V}j7;a0@$)q36c8Uxzls&+jy>i}QMoMWB=aoB}4U_#!ZTQcc`^)xnu_;Rp&%VU8%+Ndhfyj|<7tTO+%UwDibGsKl_;N?wl;k=Y$e8s$zCvTeDR)55WH)|y8<I)|Ix)Ser@W^3$-j_P*4`Rji%VXB$I*K{wWsX;4nVwGq$o;2kuJa*NTQQIw(#9ZpB5T0^v7N}cw$(xAVG3DcTiJqXd8YH)c_8<fu#!3mS-sCr;Ll;`L4PGSg?EBY2#6EUMlZR|~+6kgNH6k=@yAhGRL+8l1U*kdY-8vz4OS=J?z9XXX>A)YY!SE#`eB3xZVfFIv>Cq?0C+zv@`S+V=jop1Y)M!(*)Geh?%27oyNBajY#(`|Jv-ADteyhn=*wg*SIcuFaPMXJu&F10h38d|P(l`Ru?zHs`l)J;H&svan20G*E$r=@Za=Lf8FL{loH$R>cSR{d}<*p@Dw@ZRL>tYR2tyS2u*B!WHIvZ2*3f<w*3vX1j#&W3d{0bI1Fwa!PbSz}FSEGcr5+=b~je&%Irv?%+zx_MF92wFS%$c%5+%-*NBxMVJDSM=xlMXwHAz9pEDcF)9K?^JkJ1eZ|4lmu%7Fj7h!yv8|>?xtIm2P#_)S&djh9Z@U50$G*ZGz4YlDF#(f*}aO$Ayz%<S|%ldF@K2qNz>U^ai2Z_ruXlf^!poisbU%T#CZM>%z`m$ZEvhj5H<A3ddQ<?vg03N8L0;bk~KgkBf?+hA$+xF>R+6^lXtizX2U`G?|8NAGbahc+4p5oO`hwtsRbg@6rZrHc<qmnvm%`&+tp&_uS#TH4}mkd(okdV5+GkZ)ZQ6_~U`gK7E(gLVPjO??&ycp2<ugV9>e!8odM74*d9C+QXOTQteRU&apR*?!vR&Kw@#MNZhe1>#Dqx@J@x_5D*3=)`AJY%5XHVS!0Y5CO&2@&x1WA?TGS4zHWy4R^`6Y@Q&)t?SBb`PV(&bm$=)?Tm;nKiTnaV>4)XBU^Ge@g`FBhhn8wJ4aFv_**g`A4z}mPkRpKqMMO$!*NN1hEo5ZGI77hD4w#E-n)5n|E_6A-icR=lT8N27OX()EWWmMVMZt`AvW3A#jx6YT?9B78y&3aJPeJbIe6Gg^FIIp1YkXxF|JLdII(%o}{OG5wR_+e5AfCvJm=s>bkhrY8!$kK#Dj9P`FoU&Up_2vc;7y#n;W0mH4;Ibz2_quFSw-v_qe8eD#2a>oG*Z`Xig#Vux%~?ER>J_PCngFzzy0~d?*&;CCOu`me!olrGpEh(e$$2m=*#ijUuRB0TfUiHl@Z$0T{U?qiQO$aOBhkY<3hEt1Ff?nPJkTNUk+ex1LVO5cIe$<)d9PD_5HwF2fT<|o8E{ur?_$Qa;9Jo*$E`Sdc^1Xb=$>7pxyH>QtOGa2EZT*Twu45EJ%s?o71sOxt0Kg253jFvofZ)dGgLNiu*k;g2jLppVrtp?BSm}>}b*PHieMhF7299&GNkzwYuw$2SLo6J>t!tmlh;@&e|cwh2|4C=ZIW)R7RuAf`Vo<N6;8-0KyfjRbo^E@_E3hf<k;&1#2r1UAdDoFK!s3EVaMB_)ZG|wnh8j{Kda#hvQ2xBs(iC6gXyUY&Qr47_-l7?3+LTDf`?hEx2m@!41zS=uKgQjz;-o^RB`anvjyO0^(}K;N!0HN{6+<VQsuSEQjOeybrt_j+gU3@TzmX>UnrAG@DSVkEWrwh$uEH_F;qGCfjT_dn~d)s8@I#TYk&#8J*+Fpti*W7vpKLYxYBS?m?l^s07;uahSoH1HT{7+A-*d&fo5q0b6eKLrJv6$5U7~dbog$V-LH9y}JDwbPIa4$i5+l1z;#TG{{th2JA6guh5~(vRjCpc{`5_C3$g2__*Llfob}jv@vPtuz3nQyIzP=5vFzZ_Gb$z?Q>d#LG0MgQQA%u{xaB6Pop>hwebGN`)P0hLuofiX*jw8MP-ITg&sONJ<J&bV?Mcf_RyP-+T8$@T6tK{L*Ift%bH;+7~P?WefcgxLg;%N&&<8}UBJZtq}?63qrMl;1M`Qr1WI9{LSEi^GlaXjc7&n|cx6hw5{BOGFK|LM#<5@iWDNc2PGeTQF6C^Acqk*$mJzftg_dEB?G9d-`EHWh7uHsaaM%fOLnUGzu4O>cyQc?2Odk+S1}7{RTYt>$9buQ4MYYQ;g`MkfzWOoq`W|TQ!8Tigjb0TGl_B{nD|x}Sj#dLcAnl9Vf-9X>&AH=Zw_X8NvFA--mg8%-&4CO3US-dw9r%0hbzvR$B8sB{3x_uberElEv`RFc!3LnjU~|Bo8H!Jx(u~DVo~eC{tDZcsJD7$6^oNe>go&&%y#3XsAKcxzHCw?)zb87A<9mt1%uSzA<Dp7h6yN#gZ~n7V-C>tiJPzW}e>2C7m1-P!C57w_pVlUoq89lU0k(6{-lgAjOG_A*_#qu4`{Z=*Gj`TE+0U{I5sru-p3*7mEN3mczks#qT?8Zua<3heVY1~<$WVkF1bZkv_$98-vlJ!H2JlsM4;KcHEPOWe3txl`Sr<&`R8u(bjBSG;VaR;|(DFgp6`QwTgK!7{H(q-#Sm8cq!xi3RyFRP|Lzve`pf)WGvj-B%wd@B3wa1Um8KAqziYNQW4WK8mbr3F&a4(p4a6ga%9l-BRCqvL^7lt<QuG4@p5omfHyO%C{(meC70nanMU$Z!#uf3Zq_a+Tor0<-&(FL*9?!di7BlX_lNgi<9mt=uuEVwo}ujh}VWv5t%7Ba(9!iT_jM_vqyRnEqIUj0N*oDIP0Vy{1RCA(Q*du_~v?c*eGKbQwp4q%4Y&9X$B(QV$!to`a@0OoZtgI7{ATpka=UIj$BDY&gA(2OLV%_Z}-)g_GgxQoKI8yyII+OT5y=Mc8vMZh;l7B8!$rqooy3fOu|O<l{ZzpR3qqoQVxST>&$avzpSp@{{i_8b7*@bG?ElxwAba9kP^TDbcTUUAPe*z^y@w>7}J<HGXyVR=>H@CVDT62JGuvDwNNZ=)Om4=${3r512JYcw_!0If|2kgWg|!s5#3Gn9c8G=A$Z4N#=-JaHqB6+eGmT@vUZ6C_%IM!3;|{~x*JX_KqAWa<_(XEP`7yGaBI<NYmL+V=Ea<-&r~eW+T*DNlPzROpVO9vN0)D>Vt0+9hZZ@3>7MW0Z+0iCvz)Lnr};UH|qMi!1b3UPsEdG-Sxc?vGp{-`t+diqE~y;;M4e>-HcRdRdL|biRpaa#!L-NN%-@Uq*M%mQC1|Ou>|`TOwKFf!}?Np%<1@E=4~-?6PgqwcUkHUA+8MwZSZ)<mXP?xh90Y^TSW~Pq<s~Q)d}F0ylIlN6~N1ia^%6Y(s*xpdo>Lg#Kto_@f!&TQ(ykeD?v32;@6)XA?qFdszblbxxQM77+Z@&>c())XWDqC=hOUHz(-T-?uTr`J*ubHfY2If0(9(1ho&zoOd@PsOlfWh~WIuh+y*QAFK(%!0!EUs&#C(S=};E%x2z#s*6y9x^Et}^RIvVpZ>eJIHnCA0RQ}RR=oXd$Ei5CKf6zEHrdWrIqKgZ4I3ZEutD<Woy-~rgb!oXaQ?q$)F77qqe<iUW6~hvFKW;r?!AjSgDVc1#*Djc4031IyP7gGfxK5kM&?f=q=dMpEW=9R^xoY+Y3-k@Ytfrkc5v3jm)oB2KY4oOuul*7pP!wc;|1vB!`<`Ka`W)`lcPopy)2$I&c(B)cvHH3yx)Arj!r*0+t0litw*rSyb`U&mDBG;i)iRL=IX^wBpCl@yA#18Qa-{^QJ+F{ur2T5WxD2o!t$J6dLi&ely(tHFwmdrG`)gM-$?nmq~S&biP+1>g^?ExJX301PTC@syVfMpP<lb8lS^iMc0&{-DYP3Bsh|k_)qi8hUPSk_4oBqFeEVPCp}D>vw_p3Q-JVQ_27mGQ?E8L<?X|op*6uasHz~CrjLyd&b}D3}q1uzhpuL~|R~puVJHA-3jXpk07!_s?WYRNU7>4ZU_@3eIFMt#4dkeO71(Ii8SE$U+H~;Zxu!al=ZW?l?(;RX+kLXX&OW7|iQivP3;}0<)D!#X9FuaTEjD}Y73Zs1LHP;=^cm*-jB~HJzGwroSyrEq;yl|!Co9O5)4{z(;y@KAp{#+qmK0p0_t_xj$C-`OETy-XS%Wk$NqraI~u>0Oc^#FJFu)<=zv{7l^?LGw8?G-YhUlw-Ow=%E7&b`m~UiyN<umy9>8+Uzo$PVH~y3&txy0Yn1HrUDUtuJ^nmtLi22jN2f2y^=3U>L98Uq9T!&i-gJy$)F8ntJ0d)EhUaH`PjY!OrC0kS77bUoRwIWwkZeUo^DPKEbQ7MQFP;1FrGnpXL^ABxi_|okzYbY&-<06h<xD^`BI$-K~u}Di{9FH~;hhxxSHefp%%Y{eGujt#ZKY8{hosCmZh(biF4*e|!-?%!Zs&6KN5!mz5{9Yv%gXE@-ErtK!ehP?<!q+`_`@1XM_0j)6peJLb#_qY0{xm+sPv3PH9l3<y~>FzBI~N_T6a9|q$%)do-9IlvDx=JKoEcWgsMXR+E4k!&d1*n+x(7*wt<e9m@ZIf}|6@)g@1`jZLn@9|~ISz|1M9cOC@O1{7ro{GBHzNul!x2F{gi@5#rxdRmotVK3Fz;lg##&)MMI~%%qI{3~1{uOTiL8JUUgS*XOJ6-BxcbY6e6r7&##-w2}#MP{T0Y&k)ItJQ#T&TfBV)&FEUc-@_>8fRVw0fIri>w>t=}2{zM`~L~+nn|kqIjeM^p}1=qeph+9w6Yr9riUV27mCcu(MJ9(_Bu-VheuIy}x(3+i30YrFV88v!laL_o2j5tI=-o=vcH1#4TUKB8K(He$KRz%}C-2&|LLWz2-URZUdIXUH-h_Mag57_t&j3c@O9gvtT;lu^T)bb*E@8Y+~@R60qF=@=rWzu{#flRL>7*UZ+l?D4FcO`y8)F?>+~G@j3hE&;RcwZp&$;(;hLMbzMa~Lkd#l>^O4`vO-tkpiM@L&ZU}~OL8hzF;1$OOto~3Dq}j?jmeikGlrC&7sVhkP=4u4G|N-Vv<HvcQ8&bcJQ>R4cmMRwS3h2mnsldlS=m(I)Cig{ow5jOwl{;M>)b4sA30=!xtb31ASD&2AR$xc9VyoeJLTHKfjDMCs#Y9;1%KZMGy=Bro`69gS91Hf^p&}J(sU8l?eW*B3p<Uzi#D1y)|iCBwLkJ0k1JXH-A~=p_S|)rBp$*lyV=|<7>wQ<s6EW$?lRtg798$Wsv3(|H6Evo8H;chA~V>0le0O$IGK4jJWI3_d^2XAHR@WxSuED>xk6K8s-<Pu>E>rAyU)%~PYyqarTW?7(`V(qv%{HYS8dazy_lg;*3+^VY5lR=+?85;BzB$|h>A)>(7*oePydn~O(!n)q31DO85icEBNbRmnJZ_RiZ~{(Xb*z7{w0Ri^P}1O?457^=Kq+rXV$s_@Y)2guycrJ^Mn2K+y8K~dx+j&pd)?SINm>Lor2ob+TU$8_D-`m(n}et=BY#3T*wLXCJ06%c1Uf(>;5z0+y^+7`|l3PscaT@;LkirDo`<h5mmhRk}>myBDH@#!E3-6WQG?-2BWvBL6Q5be_0^TpZzn%?b-vcR%H9+ghDS_kkR-z*Q;7M{>?4@^x{qjH|G?VR-W5nobiLh7KntSeNfhS_c5~V!6!#YZ11q~^yIYJI^1ot^L=rYb9%npXdWHz?w_;$A5hw2p=?Fer)6W=5_W#fS^-QR^o>IU^&zbztswkj>dlN+BI|t1p-NP<I|soKE!Wr!E}jI^{5tfa6WTZpMC%RUkQX2(RsQ;>-3>+)ZyeE+bBk8<hTdf0j^j4Iv!h~8ELfTEPTM^{ipifb==X6&Td+2%2|z}qRC_#HI4b6DfM-+#=qa9Rz}n!CJr9Ep0?Qx|=?@#{b4@QP^{ujv-mVcl+g|8qFKGOs;sp;sZhz7`JU(4^`;&eP+2{;rx3Nd~qNIyX66fw4j01p<z9Om%pA7rs%V3Dl4tg^eGWCk`j3XEI2=Z);IDdWEME7;un?$J3QXtYxFO1wF``!O&|Lz~=*~5F6WvHrYjr@sXT<bQr?qJt{=T3A`W9$Z<(B~=<w~%9BezRa-I;p-??{;qV&V9K+?-<T4EsWJf-S~RJZe09949PG6u2KqVgCf){&;hJwqyL~%-^ko-EFPk8$=Tb-6Z!pd*Y&TxRYnV$d@%sz>ge|87+?AKJ8$ubbPv{;+rPteMW#+m7of3rPAW-EC!~wg_<i<b7z#y!9pC<HT;VazqD49}3^S%{ZT<Jqi5Ra4aowir-u?=G&SqQ=()s`u?JnR>o}K*mAHVfZgp-kj!NX&h2a^&#S!17i!^#4Eq53Jo1Kr6sGJdeBORoySMpL=$sD~9?R7HQklQy^<6n3Q3&8$e@7ICp&#@d8of{*;m&?|l0+;Zg(hxm4d8+tw1mNcgqpltTsMJ6t<ni4>47zC5(Tkpq3jK`)CI_S5&(IjB|QM?GdV@10U|E|8yE-;+fx`QUVZ@VuYbdbCKap<{h?2_-=0{y^BsaacdZhyA9^^QxfQpo)%ntD-r2#b|!N>AHaFtF!7y{*GqZg}Cvu&vRadJ*rFVL-g{F22-pF%9`6<N13X@z{B{fAOtub$GMw$?FT8KHVVpP(KpVmg^V?fO_6`XSR^cx%axL3%S58CJKX~Vz{Jv<4fNSVSeyjH{8zNgqbeng1Q3KVh-e%EB3_oLlEf`7lzXE2nFbE%q9uMnp6gFYM!A3LBJ+!<g)3H{QQfhc4Ks9x*d#%H|dr{T(`yqwxN*<?Z!iiEd(9Cn6qK?_-z8Ri1JLz!$NS;dlb~Av}Y-TCb!Zok5X1_dU1d*>nn_Ic{tdo0Dqp}{_<k#(pkpBI82Abb~N>4FNFbS(N5;obWEWtN0TA64C4f&w!)se9XIsjAj)Yf%UynkurXN9^r6yYK<Y?hLOWq5qxG{O^1FbOYYaH^v{7P_;Jk=+gAp5H%Oglc>4P$O1TuJ)O^7KYhDBK)=XMBXMyx-Lgk_*dN^fQHGuY(1nsrQ00ZZ!{m*ev!fONDN!1$Hv?XT@|5RTm8!<^8gBx!l<(Q@O}Gy-yK0xNmNiWS$t`O!}{vDc&`jOd<+i%j<PCJg*uw$8G|Ex63cq#V7)Lz6Cf3ohdZ+yd7K^kb>#=s`@*^-b7BzP@1%Za6;RPkL)-QR0zrft&GixNa;q&kxY>Kk!27AjWH<NFMjvFnrRz-98W8`PaYwn;&JYHd#+X5-bU5pRW$Y+pch!541N!Q;$rh&+#<I7E_oWj<k<wQ~k8MC>F2!sE=o5|J%Q0Baf4vitLNkj8*E#2Lj6l+|6>^jp8A;`;-4Qzg;SlwA*YQE!D2}`lEqB0E<VvPcNG#Z?|?rA76!q=}9J3-YD(t2+ObLo~Lp~OP!?P4}3W=d1er$I-tV#g6?aBu?>!%#my}Jw0-uol8Z67?K!kHxn^{|Q@icy=pr(22E1SHx1NEV&-Kf5JZI(XM@1LsU(T5Gpxlugv$#)trBrgA6r5^tj{`Sxf==YMp2#1p;%0vNSe1W?j1UY_J5j;GA4T2JpMY9X>`%vB`WE>M?D*yxzR2x^cKQ%G9Qqf<?8)hAt9{n^?C7+y#~!nG8xI2880x0oY<;qKc-p2C-)o+pwA&9=wWHJB#?gKgYUlte!vMA{UZj<4oIL%c@ie2Pcu1DYDqQ*c3~Y?=%oa%tD~Si-IlR!l0!YmmkAHYR`{55+p-`$o(x?a@!BKGKg}b2p!LMin<S7;^h0=@a%S!0cONqs`_S(fNE0hbRhXmU1v*Jepxx_**o`z#qm>`XkR-*y#&K_gy5@eY`@<O7P>T4wmMxGjg;x%+ZmbtEUQH(r({FnoM$ljLNcSQr+tl*6c{Ly;GK%E55Vmx(+^3h$uU<_(!LS0G3U5XfS*n<LlFncTG;EG5g=v3b<;blEH9#r_7$5v*AREwfR<iKVz>^9`dcF#T7EJd+seifu{-wQ$YN%AMd8<h+E8z(uJK0Rjln3Zd*3SR-Ri67%G_N$6b$Kef7D%EFVswQal@UsH??_unXirl4$-{zHX5|@CQtcyPJtk?#kzg2|V+kfhu6N3{K&JJPESKF#qstGM2+ks+GgfcLC4=<V&X+1w}L)FLlx(U0N<U@hAH5}9T^dE;;tKfr1fq3v0#4z0pWlhlcMzEb`Ct|K}V?eQ1t^O$%!^>TuR1R1~1uK)A(g(ng6Xesz(cvB!7Ol_DXp+C+@7}@mlCRLw*W{77mk+J#&-RZFf6#u`IN9U%xkmxiqRW=4;!jS`_qEn2N)#04QJvt6jL?K%WjrN9;Tk_gyqgr%^ZniZX0zQq+!Ju|Y5<fM5d-+QLAu@%`dsXv9G*OF<Ac+J0(1!+>S!0bu|M|x>lC!+;c<KK5O6`4YYwY>g;l%okt)soG}^7k`BQwi7)x7r1*oZS{^4h`TZbRU78`#j+ufJi67juedvE`s@yQWN@AJknHpOK!XR$V(t>R5;R$HZHJkSPNrd?*e@Wwy_$|MYM4+AAQt5C9fJc%B6<Z0>Wb|AAVbFD|wwprcE!so%D5y4NCVZ6fw_^PJN2Sv8&0T!NPJrlCcsugF0XQdwhz|6X+mwM6zGpn1TIoxj=PbF-F^qYFJ-{#W`R5LTn(XuoL5=^ZLB-4H(RL9}DdF~)sW?fPs&+9{L-16-p0t$?Y0k;Lm0A27gFvu5_0K8>9x@~Rp>Ur9g_-(c!;fhQ>xE6KWk=a&AEX>?cb*-3G8q=w~q+%_}!+1Zy&mdNSwfgQb^7I@7)7rXOO@#?EIw8VyWWyAhcqt2rLn6t{F&o@Wfld0LA*0D5m~}J{xxf<ncFcvm%1O|JZMK=0Zx0?7dz*-Y6l2t#EXEMxJ(n%E-i0kT^Vy<4lP%Woz!r%B`<B?kab~bZy|R(d7O4g6!*j@%$sy>M9!~TrNS^8{b_b*NkxMe&zz-SrQkclyt~f>UgvF1GUevm2(Nmj|p65+=hoD~+gU&0t4H0@g?uRM>8+IA=H6mr&@83|_64&8%V6d$lO%8^E8{@Wxbm&j<a~Q0$fiI!sP6RnV=%Wdmwh5qk0F_+Wi^4`nCZeXT|Axuo_5HEe(-UD=B+=!q>06pUEaE5AQO64rAAKXlQ!9RS0Fpa~eM~76j7TCSc;sFeu_OG4KQ0dZRo2fX!{PY<H$>o@E)-q}B7-1t@C3T1lVcGwC}b`rCRwG&)QP09-6`xdY(AfGp#0~y(Z4LHoYe~@CAh^N8E6S*GWX#RMM(q~aVR+DXf(y|n*QSkU3-(Cf!1NHmjRCCqh6<~|G@hm8aRAjE%}+iCLkR6TYY#Fir8bfI|y*+Y%sGs974}~vxe~<Nhn&V_`vYjr~P77Vmq*fR{e;U=!3Gj;8R&og5FIrbg%Gp6&B<X83RoVOb1WZ9;-|wWNL#@;Yy!jLJ7N2O9E#ff6N3?WC|ae&MQ1UMXr?Tpdh?8CYz-%D2W0s@Rx2^2}k*TbCo&k)l!C1p@t7@s&r9X`)%(#OZjSuCgl}St$+^ONXF$2^fyoqN;A}$Ea-X(9lV)drcDdJ@R~G`QiLq<R=xn9N(Gz&va_L~p3<T$$X339oJu8qovl~XkaKai@=eG(&W??<p}`5Ej1aYS0ZmIO<!X5rURJ&a$w)<Q6SlEc3olJY%z&$MHK<w|P;r%Q=^$<0QtPdmB><X<rA#f<m`hrY34*7jEiR>5`m5FDbP=<Sc?3<Vz&Y?u7D}ZOS&a#s(w_~QSh)ghDmB}xRLWPpE$r<AqMdYdt>Rd0k)yX8@-?$ex-WWO9opI|Eu{QgeVI`<r%6kuqQs-I=gVPw@$>q93Mt|}LxWKRO-Xy+MG^N5qex%CKjKNa*okFJBz$D7T4IF~c4fKrU7+P$F$1qyQD(4JX$DJKQ#E}QL6G8rCDZMQ-x~cyE0&FHmD|Y3Y{Qv%hC)Cl=cq{MBDw;ArwpkTKYOV+m-(zEUR&PP0nZ5xB2tW3L{1n}il#Z?k%>qb+7cd~7-u%P0FDKyqJ#?L*P~kU%%h5vp!D!NSqesubyM0mRRc0vvuqkuUmNP4{v$Qs5|CyKwWfs1K~UO{D(7`=HfPyREnw*)2sJCUwvO=Y#=2x%U+tC2=Dc1yDPcnsDmUC3G)yuQNc>mo5J3U6jJ+0uMlJ%i5*$*=934B`NNhngvk|17LN-;j8znGP=4A`0m5)$UN!3cN%GIT0l}nqZ?RCyBfuJ)Ixqb(jZz$jyrfmy&sssYhNW@D>Tpde@oMjqMG?a8U5jvHsO$6JRo|*<`0X_-rv@+L5tCg*49%yGCXeR@-lMUK1=G%IIl7|3|pPZn0dZ9pN9ROGm(?t+)Rw`~J2-kYjK>itm)l6PNY%D)dc1h#z87C6<^vNqp6DdElT%$3m>x4|5aae6x`Pf1#iO;4DLsE+alJriTScr0oap+q~Uv2U#VV+!UR0U;Awa^ynSYCbQ`%xWB%kF9jXCqI-(Gs!_HxuqL?Y0JBBagVmOvpM1H3dnAt=Ezzb_pd;><n9r`~XM(PK6ydPnlD@f4|1o==(;U9pZJ`Y3z|Pk$sFI4DbeJFb(B-f6*63+9R|#ewZVFr6J134#q`y2$S~Q?OE1wvU<Xt((=npeow2M01$L6?=XQ2DV8NPWs#LdK&9hf*`voez4Em1k$c@h4A9x6vXQuN0A@9>{D2ol=NG~=QN1N_tYsVQy3(Pf+X>@hoxDN>UeaFYiZ;72o<*2eYz5a+DA%QbYbatw;kO`3BTqFUYbtxP?7?cf1LUtFQC%_fOC{YLXhL<bi_rO+vzpZk6_vI7LCA_o9-q8*;NuaiJMg)(VpAoS;1vfbY6u<QLrZ5Yc>+E;=DLlO0Jt64e|WGHgP}z{>m}9+J@>T<E_MjoJr?T#AeGmGl`5+i#tK1~F2H3CK$w|h?>cTkuEY-u>%e)wWH?^x9x>KKwJ5?+CPjB1D+Vm7G2p|*Nd%*&3K%eCVS<xMAw({RM1~1iF}7vJme=FG7A(DkmNXMIVho2ng%Ma~VP}<1BL9g#Bg5PYr*gxN%H%FnA^bx)#zrlO8ahLkY4K6~NWa1k3{oh0k=Nt$MAmcxOc6nqj4g4}Y!Tb#tY%8D++(ViKj9QO3C3p>k+KIH$(C4q!gH_B2^01?aaQqW98_wW`{hX7>Uz8Yr4#6q;0Z+~oSmc@(a9G{JyGbTv86r=boz#Uk`SneC?d<wm=unv;(V-+f^3ALIxs;R+aq;K#^ulYDmGPmnaJQFHVoyGlz~tFm%MxVB5A#vDUwEhFPU!ud<Bmi4QVm2lK?@V20L262wBKCrY+&C5{-HIVwmp#-1dh$jX9|-mIYNE*c$b~GuIEFdI838zOjs1oE#|lY&(xAr;mTfi`_l%0t)9D%2LGvTPQ9o-jj}()_i}0j{?f26Xva`DeW*~%ub-lB(ZWBi+KyFdjdj1Kr?F6yguQWPcjS|DJgQo(N5}RA`Z(L$>)>Q`gW2+o|0P}ESFDMIDw!LPm8n`M?8UWPx_|XQj<#PbX0ZBY3z^9qL7eN6ojKHY75F%s*`VOoWT4^RyuFffxU4ko1QsIXEvuJ$OaHAP|yH7aCgx<K$T4kia~&+kYx}tfL$N^<C-r1$mk@SC<~bYXx!82q<uHYgTS2mz?>PtbZDG>Y1;++ZqmXe!xlk(LW^fQ)4<lb3w(#ecQWCd1Esj->YUv26Yg0N3va^kAa}2Etgiv^8jXIM@vr!NNpA;CdK=AV=mf1ReFk04pF&rbKD@bVPbmaavSxTyttcZLWMb%h+PqxT8ZdCwTO%u@i@SnJzB$5dIJ`o>aXHtfNf}-_GTTwvdVbBq+u)hdv2q<Fw}X|#n%++{AFGFsnXii?;H)#e@kp)Icr%8qI(Dy<0uMAdd#xz0`B4i|Asmb5c1ZHxbxmhL+<{JXTN!ScctI(NSy|MaWSGA6mYsPmJMX_`-e1KxijbNTr)Y<2U`<X8j_%?W9gELV;lQR50fl&2!y6@PB0jXrJ5=7$$~#th{XEI*SpvF-RYoVPxWWUGrF>nHGQSLCYtDOs;VccqF=2##3yrN+Wc4y3Xq9x*B^_SUu_miq<FYZV$tyT>@Uy!Xx{iS0EDFIMLZPYBl&Wq~Eu#f5!k*9A^I#v47^s5cpMH%iqP1kpV*zw#19Uh*2La-rzQX}JIRM=n->TPMR9^y<Hq_7BON&-K!x81w&)Q3S<vI$wug?c)h$zzP&-r|Xuil)A%gTh3w`38JMHem6qP1cj@(enq>>vU_k&?W9l(!&>b}dl+O$TGI=MqFDFVY6Tnyd`ehJpE>J2JN55~)=Q(-H}!@IAxGs;FQjr*X!qH|S)th*lmCaruo5&_ehXAEqv87?^p{;B4SV9_ZnT8cpV|VseS=jgxbDi(3kQFex@8t9nN0_O|7IWmUJgwa2`Y+6tJtv6kCP=U(aAS6cq4J>JH-s(!}sv!zaGYTNKn{c_-!a#tS*FhuUKZ7T<O*5Ow34n!zdwdRl8V^~TsR&iFrga_2=A+9~!LV-|-;fS;+I3%D5auS+@WS?k!sV-m(U%dpDb$F)tpCfE4p5vg6-o0UWibYZVO-gGSHTFm-{AAQ!*IL8n4RHoZM4b*b2v<S)8huF8g|4(x=y76XcC<`9+tl-1EsqXW^~}DOsWv#G8ep!Y1}ln|O}TpQ7>xzGf0%%fE|Ylw@LpnJSklcNn65=2X06`iTO(o{O~cRE098gmy-((Rl5ZWzPs}5CQS7aGz?J49C!dF$rFh86<RM4!kh1^}IScWSGmD3u89e07;vpxOhY)ieHIs)ZSFfGHLpf!#dB~Z~L(T#`<Ye=ZTtb%Rpgeakg5A0T*+&*EkXXex$D>t(`W#{459%6MS@5S^Js9^kL6llI6HhmU%QVeJ3s0q#eO`bl0b}7>j(J8S!gRlxcXAc^7kGhskX}FW+-Dols*Un*_Q@_{qNQKKRr`O?{cQrk$U_ot{^7$gr4t(WIP`mo0W4+fL*>QjUwR-qQ-9cN`Zx$=?mP>IfUEE*FHVrm0ibmStb}_K7h@|$XI^+PbjPnzmBDBF4#%)NMpSjnChq&G8t*lKHvPK<j|@?4n}1I`sK05Ud_lUUja6idq<XNBr|gg-BYv1;|D$|Of5^5j>V`<I#yG#ma>hC|@l)?C31#lzse~z|Oa=Q1cmKbr7}Cnz9jP*=)G~Owl>o|-Ee7^u8hTwvT~9Fv`ys0u%Iz4`ShRHWToC7`HFx?9M3E5^fb)Q8829=i=JO6E1^{^qK?f3MR@9=MZ;~iSD)Qo#-OylTlnPaK6wD8vBRcJ&BR1<e!@X|0eeci!3zNB8sXJm*h(1-gEfgbG7QHA@4(=Q|me$EEY#>uW36E6^cO8S00uuJkPHwD9ZYV3zN#TTy_Suvpx3&uVRPCr`?e{myK(s13OIlP^kJc>2%ncP;@RO5r%br1ls#!B&D&^WgLU;Doch>nKUJ$3A^VlNhTt{xDbqnAp!CgYlPePo$3SS8A@HIJdWqOi%8k!uVE^ri!ttRv`1<fEhAP+)|;U#A(aFevVp<>>3!Mwz{sv(+v-vd$_Jk!w+GLeB421r}(aIuvI&IE<EF#)-bZ248Ql5G_emGzO~07{nI$(br!t!!<QX^=#ZA^ov>6NBgAepyu5(QAK~6}4Y$vJkG+*7_eIm>!gz!6^2{MbJMsR;|8Jg?k!mnZqsc;5vtDI)f5jm=7r#s4+vzJv5PI+CUIk)9wKnoV#Y@Zb=v7y9kx$7@)8lgkvvE#4Mq;g9@1D-ovYqfQLr0h@3t;5VJRqFdUt`s{$otqAg@(YC|{aaPeQtcKk^ir=eb9#Uia_uz;C{p;cPpN+pXrIj9m&83HZ@7-w-rE+$uu`~o-E8)4|)P_s6v7b=}~G>_Sthx1beh8=`aKsNVL(yAUKgDZttu{a%C^P>tR@Ra_oNWn3+{EaR(Vv4FrGEQfkY=Ryy{FhkkQlqAxp)uQK*0SMVy8aMm(9pZFPM7esU+5lXZT499>|yKza1dj<d`e`VlCdeS>eCWW%b|t?C2nq6iPq2p$bD|GOXl>7j*DJ?%5i&vItK?%Zlf>LFh7}0hyk$%AUe@PlTEeISVp5bpnAjXt!WTm94xH>TpV#hjzf<dr*d)_ZXV+R|CCC0i#U5=wK~=vNfMH+$RV{>3GxDYVcDpAS{jt7Os3JGSWX&%wxJMD4*OX%3jOZr$}fDD%h*{1jwB9nssYPPf4k63H6g1RV8GQ=-=@2zgpg55dOoP4r2Wn+Fc*~37b!sUNwq|OGQA(uBwCX8dc9d=ugWPVvkDmoa4f!!e`tq+<{b1~>Ti>t8M>H|WgMYBIeHH{d&0Z;4{#$MPf+H(SMz}}$zv==FwyaCGOQr!hu-+YLW3Tzc`Q-Ar&lyQFf!Lks%^A;Gq)T?<%>fZDNp0b*PJ6?14oMOD|?+@V{uClY8{?3i70mW*z1zE<rVfd3H23+`U;@xePge5(7H#1Y+yx_?ZvB?53O>cASw)ik$WAzfWFakE5$Hv%t}d-n{*NKV$zC0{>sWj(*|fxjO%C{{;dMAZTPp!#0^)X^Qzv@ZT$zIJcPHHK)esRljunhddVch+xWZvi&gI4OMx2_>mp~xCg;#q=3U33yDPn!>?zg39hCqFQ%QVFA{F2{8im8t;+V+dKl~w8=fN<bh}s&;fRbvzVtA*lTPUVXEKus)RD;*EdTJ^+e6L{Ouie}Q7BaH*NCvo++e9)gCxX*X%yUpsQZ`H<_jBn*kJy;|iR@WBT42VibJDE!Vw9=;y4IxhaZ-*<{Z;pnrin4Wu<SPIVP<&uX(eb2gcAp7^6)#Fp+GW(47#Q>i3**Vp6wX_VGr-YTbnr~Cbpr`S&m~y&<N5+v3RLui-{YM)3HDpR&do`QZ5U79Z}(bj6~UyrgdYVPiXRX)`)l-64q`k?QW077lCWm&|A<YpD%?Pj<O-}R1Vfxf-SjOASr;MEz`pU;ObSKYZ5c(rkX7pA5K8jd82f1Xolb8;8L|BudCOPbF4oMf)JSycXCO)c-196+#|myRwjhD!tdGKv+E_bLhDWp%w&oDnlVR!cQ|al&G$la5k)jj^l;Y?yJ;E<Pc}q0)qOk<dv4h>X(}P8Ro%9Wsd7eT1WVa;WUY)TrQ;QS5ynN!y@Vq!>I308R`>X42E0}<(YvY5m5e5C1aSVj!nm<XFcy8J8eG*NhN7B5p;em{Qn-{<%@o#gP4~ujI9{uw$y8y-DhyrDEn7GIQ<B?6s=&Hgpk~T4WLDUt0Dd2TOe?}8_~DomO)@TF@KDQ;e5(e7V`@@=RS`JxT*rx#mU{{xq<};RdT3%J8^yMCWJGrxhKszm80kGx@-Y_j^Z{r!RXWm4EYO6u9#oD0CI(!ChGzBPF%FDI(e-SKmhVc^@}e}&YE{lSQwV8dNaX9HC|NpEfbSsJmQayVRRu}5&DZ1)dIz>%VLY69x#{=J=YI8vem`bM_!=<Xg&hugknuHkblPA|e0w(hkQZRZRU3|GW9$xZB0oy@o%Bqf7h1}@x*S8>Ug?EqUyRAV6=NuRPjp2us|+yW6Mg<=-mc-U+}aj=)~PSKb*ruW%=2LzYW^{?YXY5do@~R+KUU_Rxe3r2C2gRyj>S!&GfKL$VA{{_p?!CN%H_NFJxsa$>)7VF8>KG-BxvVWv93fIw;{@)y1;*i9>NoHyj9&*ew31NFXK7qf8NFp`S(9~u(e?deRYrXDs_kHDs_M9c?Rnz#nknz=Nk8eP-xIiHjp1<j|F}CNKprabVh(_0FowR#WOrBKwB_A_gk{=FbL;`G7b!vs#o?c22lh@A*;mxI1X?4iI`SI8Kn*VNq7s8e#d>YI`q9`d9X+O*M6*>vSmW45ft(g?9lfPp0Si!URRp28^-nx0_@ys(g_QTaZg`6B{5bNenxSi?vXc69SjnbvS{A2sy~S}ZR(!#ztL?+`93#B<K85aK>-jd-_+q5l)!2YlZ_K7<tIUJaFf%Ny5+{LFj?+aLVLIT)%X=FBgsNeT$D_K=T2sF;uMP}J~WI^@|?(ZnvF{~Ia<QBsVK7|@kl1nzPt^}f{BN|!Z2gx{T5i5mBA)T-}f_?1~Q(m=xcy&@14-yEM*))9$ibrFu3n|O+C=TS=!{Q)QV^NBW7F>f1Yx*kDfbP8%}l`$x3;L7GOM|NP@z~7|BqkuHj#&B(4rwH%)rG!;oJME8}@^mb*VM<Rpc}^#Jo8uZ#B>U^(i0p?IF9n8>R~i2x)giMq~BXhJF~F|?Bi!j)7}y~S7VXyl>LD7pZj7n$j_&YP~T^9FTlJ;D%0)#?_{kwg)x8+xjfq?*23M$ZLmXd1J~VqK#Eh)MC(KE`x*;L<=tdsPmf{E}SZf%*1*e3;!8YHxjy9R#5{xp;sfex1|`IrK19jG|?T3SvCS-{0Vq$%sP}5rM2cx>kcl)^h5Tj`68CG)$X(I$}K(O`9ZAWfu?HNO^YRUBv)ko3(1}#mT+VOEe(C_`MjtEaA&M)hf<8x``Inq{pu?OQJ&<zJgQbH&1yFOX&mhD|1Tp(SF@;i5q+7O-&T3Puw9gUC$E3A8{$qpSVHxNYr{<ZZKSo;cnQca3TgkCB9|rPqZ;V!%c+S@rQnVqk#!72mErY(VQWirW1^j6rFfpkFXY1cG&uT%TLIg;5&A-UHL&G&`2i8?<hoS)%<#&nXe&<J4d9gSg`?mKS+YDiyac+-)mpfoOB$k5y<*1yTVO&g}xudGKC#B`}OECZ~WtrEyQ`oXNC|3xm?>Fp*5$Ntd(@%mHwpG?={95?x6|8NyBjDpM_w=LHubj<WPhUQBmTyB3m$5j3|CiF8ohvdduqfFwiT88$$b_RlenqykpasZp(;RufZfZ8|ET4yh;zy5JZ*MH#(YGH}4R8-RJmBy5-BOWaFlR0?gShV}Vgln8PdXfT)XZdU;#(u0Tr=m&lrnBo*R^=ZX0w@-96LrG+m_z$bsWN;_JF^wxRf)5h`sN$Zpy@9*Azb#l0Sy3O`rQM&!Rao2YltWu#zSFyq%V!!*T%SKZ_4%pbc0Qq?7vS7+wyowPp?;67i`<DUx=0`sjZ{$KJhJMc*eWW$);S(3o+Or0<);MC{YaAaRo;=-VyR;-Sxg=6+aiH1)%`8-nc<O=(wZ_%1E?P}`-bV##4KjVvxC3&s*eyZ7D>oe5w3F-R?cWondL9oW-}7QnB;B67%{bQh^e#R^9D4MgCu@vjzx;`~oWt-XJ*43j-{XZYvhnRdkGxQSXV|74Dj(&pAA(M5uI#*N41dkzTJxsO_L>wdfm#irb~p48Y4TU+hOtVDdfKIsM9-ABi_|hfx}i*cN76QW-tfY`{e^g>c<h4g_200f>_ust4fr~eCNFl49{3Eseh>nT5QsXt{UyHiNd!&N6WvtQZK)h0p7Co}8u=hGg1Lci6y8`65KS{P=%@A{k3jO&Hr|m)=k6Qv9yLgc*adu4z#Z7_bX@=1WyJ#D>rk_mI5_aHy<U+nt`~ra?j#JZL1NNWGq{k?=@hAsf-5bo4{x{|^ShPv8VkMNRLp9f_2fLBLAQ@g9RpUqJ{^K?=(h;&M8o~jWO^NN9R?5_dY3NtpL)`7s6J3+fC4*#Uf_$PVK5Y&$twcoMpGCEV!QnaX2^i#!I=lOQ#5S)7h}H<(s(SiF%}QPDTw+xt%_0|m}j^-1sd{)wviK`C0p|ubTrkdcO>1j+h1Y`N#=I_5%qTc{%?QH`@pp`)sHIm<F~(teoXM8Q19Bm@IzGU02x>#fP7td1QIg>g=Y+Zy%9UuJ5CXf;xsY06I?FV*vP$sG5uod!wM$5j%14mpdbw08(3@j4MEh>slj{>6q?w3SaQ$kIeGpLJuPQI5&rZ%?~kS^ppHk~x&2u>=QGY7ppk5gc%vSBT4V6Xf&TRTOTRaDhoel1*OX64F?>;qu<&{j_w-@>36yul1yETt5E<UgAg>@McS<8`&@vM{c%7Qo{Dnq7M~D7ph-;%-E5(A{4MwaVz&gVsciOxC`6X=aXa@Tu3a^F2HH!`P{c^b<dL#y4O)rpYcy}BpCp}g=@Z4cMxIrNN`~-89At{3#`hJ9-MMix)*{ml__+5>?aI+;yWIWN!tT%ck!ML%FX0&*ym;Yd#l6i6C37>88sa`$^K+E|uv4n3YUsr{hb6b3J>*qH8T~+3mZKhdXg<WNvCDzr+699l#Om%}=EIGy{YPBG>#U+2a2x-@eQP8$Qa)d*7q7_3UpnfGd#&ZkagjR|Sh)FTp5Cr`;e?z;?*_JNvauch4>l?;R$5#cOYa0=<b<;`W7($+En!ngZP26YZrj;259j%~siJV_gG#}#O=ANXSu35GdrASXs3Uemi7N6-m=oF(oOMT2L>TG9dl-eK-um}Dm1=GH%O$H0PF(|iMSwM`|mH{y{KE<LzE*QTN(00Y$@7#D<Hc!1)_A{Ne1j{A{ER8`XBcd4Es;pFpQXM-g0I@kp#h?pf15jv3+sX*0&l$4H0bgSHaABfKXFFQ9e!JcsUqF|Ub^B-m#F!%eR*J2YymNa_Cs_?Ui)&0U%edmWZQ81AicU1^lulEAdmlx|0FdR;P`J{Ov?tYz_Lx+wZOdY%UG@hN-tN%rmt2@@kp$3iL~MX-t(kr!(?8P&2_J*(OWO|>cwv}{R!!s3OKlyCVo=&(KDW_mKl0k$QGGkHuw)gy;;|H<?}-H^s~krLegUWZ<893*qYbJDYcDL$J%kIYL3<bklW1F+QS6c7%iFg2OouE#hlRF`O`_|>u~>qigYE&lmBf?cW2PKz+3vvWzJ~odXe+pX=}uw$I2Jb+K{mjmP&1q(usHf=IC}_Q!7O%btE}s+iYnq0e!Hvus&CD7nCJ#kP4|Z2)k>>)wpG(lf<=bqN#UgGI=rrvs%u&*uPNv)g<7dsoK&!^>u0`<=9QIwbL8VOSG}?+vJAWF1$D{14@8~m)+%IBm~nfqmgzo>e)>fpjkG29r&!3yy{>ZD+&SnTr)e2eZbS+a)2wr2)gf}P=yecEW+3XDD*AB|3D91+j*1wd@Q7$CFJzBSN~D<h<K!Vn84q)!ntqi+_f-zMb|nMfSGoA2+3~u%ij7h<Uqlf$%gPL?@*X{=G1v3-4zDI|Y=BCM$|D7IS2G%Tu9PF#8xDFEaWC24SQfuHX?~&5YR+7KaTehhCyQSkonO%108%u5!6N}Ti)S32XRwr34<RkXGdo1|l|^~R(Rn68`PB@R?TQA@uX1tzw)w_co^J+zOyLG}OE_`|pn%ru<`<BDIPT*!3O9z-Y<d?I>5<q~Y%q6rm}3`mL?Op4l*@|*IQ#YkaU3=H0#7OYm#`k(SZT<un0{SLr8`tUonC)wj&^TyO~-F2PF$pAZ-Uoyv1%C`G)qIT8cxO=2?*sL{aqmd`2D7&?o?!5o+5JPT$}2s&O3zoE9gw;#!3^N@2Jiv=?;}or`J;#uX<l#_dC@64t4(v?0$#3-$}ZkTt6Pu{Tb0=C|s5u{^HtnT~=I7b;P}hn&rF9p?)#pSXAX8d@<ozRLwy!Uy>+(p&{{wL;??jsKs=psa9#CRhnd1qUi739j!|5)loPm{(Y*YPer=fGiJ;x?Vfr9TunzgTOKiI-G;)FS<5H<3!EA&^sEJ7&S!=EdGoSlHuKi_WlKu4MDh(!nX$!k9F&2B&;pbkD3Kaxu?67&By(PT!AFSZ#TR^pZc<M2lQ4MoBtHNI9nKevF0ltNNlAe$y2K%!8<BQ{<4CxqFDCS^pU_0d3dIhQkhjaZCRO}~ir?_!H)ip47kUmB$2RWK-xUII5C5980t-G$SfgZc31ljnp%bSumpE$fl$0DQs_9b_@`w|skx86}nt(-D5vL($N18YdH9d>&jafX4I1M5W<-^|<0)WJ6*u-hfB2FW7X|rr>;`kEwhN<bb!>U^3O9Xrj+dcdFAg%fDYTlAsGCBRJhY4jXT7w_{J*f2xYoWnzNU@;NDYaF8at^z*eNc!#W=$kP2)j5uLXF)IfCC@d!`c=GK;yKZX!f~IJZ=MiJ-iuEXuys!zWqA%17!t{-A)^AMUiD^HVSltp6^i!|2jYqr`>5Mh>RlKP7X!r2Egstcm==&f>vk`N2hSczp32F>!x#oX5HJr8v~T2Aa*8lFFjEj3a_xHJG^v5qe$=?4+YHht{b;uGmcIIK~DpT>FBD7Cy+2m(c0m-XJiToB5`2T4g8*V2*L}f!z!eZI4}FuC=&*qfE%|8=RxQ8YqWK*9r&?PXd2<;XN6;LYLbQw!XrQ8Pn;H7@+VsKKW5_KO4Yb9`ooG%_)*exXLjf!uRrqqPn8^YhHY+3`eN#Lk>a;sjW4D{I>MEwY3H{;pZL9m4=_Mtn_?qkN3jEYUIhJP#iuoP4r1}C!;VU3aST8#OYgelK@jueN4)rX$z+c!chVMdNDJTm#lOd=*}M=PG0vbL2xAS8*8_m@d5wMZ=RakiJ0+9cTCh!;Ga%JmJZ|5k!{p+D8-o^k`!n`KJRwS0eA4!#01s4}r|it_h1eFp@_73*y-XBOJII~z!GIN}Q5=8}yT4(U8bIT`?SLMV!{hK;#nE9Q{psBZ5m~h`*D=HBrJB+Q(=dou`HTj3Y7B3Gb*ae*D0kDA(Si%#{LOz>bc7)&9tUygzbToec~n>`%P9?`1SKzl(MksT>RLQ<wLc-wL3Ch<P|)Bg=TsmgZ%!RYM+eG}IU_gm7#0f_o3~$sR1U0SbovM7@J`os=!WbFhSMz46A}<lboW^CWdFE<zKa3yg9WUIMfau?m<@Yo&cM4SWUgcP5|2!a&%A4fT3*<7Eg<~XB)LXJ7u3<+0SG@}|GmQ#a~={;;Si!Y^odW={U~&Y(7?1~QjtHDPV5!D5~qsi$_D`LkLYcY^c|mshgmTp*$EUcu6$lHGdmQ4T=??9#Clv!7a)EfA(O%Xk6c{_BT~sb;e;45A$IxLjUt+Tz)F(@Co0~K&>ahVj(JeD>)-yuE_3B|2;#^U9fO6K6`y-LQK%q3Pp&2elWgEch=n~XE+=g~8%5=Y&k5icv3mB5Qgr%^v*BO=_OJdM8gogK9;zc*y=>o)+pqC#4GRC_@7ec#+~u(r2*|V`h2jHP%SY~nivRS#vQuHvHz1N1GU51hbV<Jbg&VQ@o?hh24{>&U^B;c(^cxP`MD|X5?bwfpn7iwS7cNSNbdfI6UpUkOVRey+`6QZJbS%<E=a7Tg%%+8kPDR*3XlA*IM+@DYU<a<YUXFygJ@dk7LI;p$uFkN!VpB3o^}_%!PZkdFlV%HFxy({h+c?M1g8trW)D3Cw$+hoy|MbmQKQ>B;12N>mzKcV-#v0O3iK|n^-~H4rZ5yi?HP}X{JKiR_(!+9-uxu~|DJaJW7~n72(RAYCi2=WnnK%sKHB7mJ+gyjP`|i*q#qIE<wSRuFe}4NPPIeDbuxZ|ud;6{Z-Bx4o)LJQ_D%~PM3Zm~pMBV`(vlbnUF}^$)b$ZDKQA=605m(i)N*n8{!*b18Os<ZgaO0JYOO$;{&DU*j5)tuRnlst&{zv<F|6mvD5UsmGC-gbpIL~3(-`Hg@NapZ{`E495_O)J&d<hDQ@(o&((_NyobWpszAeg*WMnpvY8jnM7e~xOR4wNRF=FY0-ol$5Q%Hd$gx4#-!xZ)D&Wnx-B`5-mj+h3tb)E7=Df=8&NuEs9cCq%h5_Nh0lq<caqWynT}yNT4`UE~TKc5sQSfs|M&6&6b1Ia<Wsi@YAl;O6wg3qgS}dU16@9!Oq<s}=^A3fO)WSM(xuHd(m+ap<||cZmYnU`O#<@#OUdHP#Jc@~shl{TM_}>|5-JtCjU4a^aLACB5;b4-3JXa2f(FsGvQe+{P15;W5>e9#h3L6g&Z&tkI(2k9<v)ph{BpYD_$ICX?Eip&MaAp>>I3LdDg`6btd?C2M5?wa5cK21vcaXcc#`sQ`bT-~RGq>XNWBq4lS<q1r`%p)o0+7=b9pUO^vM*i*NIj~@q7Qf&+bZtKJdBEJhAbd8QNPwRkkFN?^>X@oQ%p*<DV@-g={!yDa5$B4T;^>NhDFKxv7(@01P+x=Lf5>c2koQ8bZY=1L`e&ZyUc*8@FFb4kUavjTmgFgf+<eH`CKt^+X4ESh!s7n63T9wh^vID^R7$C0H;}!0OeIY1`jr8)|*}ZEQw?-~{uZ4Wf(3=+U>x5zsqq`yu<40+%#8`?c(3K-8I<-w2P9mUTHIHZ$27?SE<YIZ)njuF6C4}QRi;2NJ4VgaZR+Wq`jClB)_AuqfE7%o5bIIIGYyqse{>_hmvWde?a$!U|pNoWgdK1E4*4hnvuz^%M*gl`1#3HUx#sYQ<ns<{BFsdR^>Z5+b79p$Dj}KC1qIhVOX||3M2}AB>+#YfJlh)z!shx$sYS{1A{>klM-2P9geDsUMDRzGQm#xFyBwP4`yz#<7ZufOni40@xgcZ5y2hG=*g?jBlC$BCIhHx*zk^M9UK$sHR{ZVY|YM*bjFZ=FWgd>dsUv}R9_SYJW0MsF2oATd~oIVLI0~{XWQ;pL=_5%VRSyj0ahzvqKWj6wLm8=3wJ%B@*5lwN&6NsA>!V$w8=UB<kB}$n_GU1SsZ69l5oGVn6Vbe9sKE@TGJDJB|D!`(NWM_84Z1dQqmt`E&QWMiyV>rw*jG+l>o?UFFQB3pao?#ZFuX$E6#JIPRS&Tc!kau;4Q4ISs!x}cr6sGlp6+bP_u!Q{?esUBTMe5ErfSu!KnI7GmZ~r=ikEHB^#;+zM;L6HFuVCoVMa^D3!savXP+mL$wR^77s~H1!ZrIDWdOh>p%Ns_vuUwngGx*?IeK%gr=9P0JDBIkHksqT~nxC{Yl2(V=1}~%^+Pn5bAC%U7dlyj{&0SP*oNw+TK><U8=rDQ$W}dMtt45Bg>m=Z%icPeS<k-2+@sknMw3TbG%$u8U<Dwvh<-IIG+|-5kEsjm23tCE4#?X6Fo~di^@PvJzeo&<hE7!T}M_x~vw_qT%jayH|#S*00FoqQn({pTEGfi6j#lC!_))Sm47zk;GLF)<d37N98IL@?X(U@^Y!djWuEZ!NQ!gH^~&Vuf1%_?CUvovd_Y?nR5yj)Y(G5uipKzY6)>j_=0IK#9V7A!6XL7<m$tAPfscd=ioTlG2StLMJPFS_;WC~$jZyn>!(+pfHjE{QTX&vX^v!F0v-pccR8G{<!1Wt*;8QD_@8j8<qthIM9HgB5?KWR|&#6Q;Z;-3?C3cl&)=tDHSXOH3Ji$d0f84AGf*2%aMU%(PPNpX~0#+!nWOg@I~+Z-#wp?>O<8MRqvEC=9|<HN!+D9dJKJMrK*sTZVl~u3zVLlMvhD;Y4Oyro4Q^6z8Q=e%~YCCdF-0vhjSIlonJe&m;w%UDZ5{Kh`2#q%2a}6r#cz<|w?x&Q%HpGi8rDoyN(C<k_P{q2|QX)WMVyN>h??-1SHeX*(3x(^B$BvqCke7Z<pf1%ZnxX&V%pofvl`M^hAR?9)aljC`Qn*Yk}~d?yL=xBD74Kiq|&Yb+NT_9yX7(}Y*bG&?1i<WRJ;;yLW;ZW!GK27GdiPD1rL9S?7EElyn3;VYIXm}zxNuLfvyLcJ1q?@k%oV&C&IJUQ1rp1RWuFVo<303WP5#p}{VYL<Gm!gjf-gM8cp(k!#n&_y92x<@7_)U3IJoY<U@T6Fg<a{Fk6nJ_3F4?N>)VHAk_`eVG3h6X2ZzL6;cNI)utMFu5oiDK^a8#C}rv?QW7=q={jlxo%T$RAH*W%MCRh&d5o1#F|tFLp;7*<q|jqh;k;Mh2W$G#2Y+R3#V%a0Uv%kmMVWg#FJV5029|!y-%=jCfD!t|rBDLv1RB12&IiqP0BNas-mE?_c2hp$Pynf28Gz^ejd*dm*Dy6Mo?|Nz6oC@0o2anr|!0w-lY8wGNLPM>(dV=Z*6dSn+ZVMTad6Lov%xq$?)M*kihhqzpuvb<`F1d6pqV71At2WD#PP{*qxAdg_fmalw~Ma^OhCLvzeR8Yl1^Mmf?J^d0$F7WboS9v$xOpSPQ5`@8rU`wJ@cCA34TKHuf@IAJ{xL^8MA^2heJ*(L_Xi#<@@YO8EIrUCiwuM4aE7H@`oO!0TWfqv`P!MR#S>C#T6TG!*L$)-0&)3vO&KPTmmw=N8Uy}&v_;EfAG$luDKj8yAM^f$Y0r<&dNS9aU3aV)`G)>jYNypz%VDCkXxc->GDy|N+u&Z7|$0vP08;Xs8a+<EBh9@73K2uFCzi*afs1|sd48W34&+6%=rJ@~bCg-G2%WMeiD$g@}&?0?X(Q5vx1gn!7y#|Tg)QE@7g6KhTmDhWxBKxH7uCJ#0z$cr6?1O4W43NaNMH(OV)8Pg+h$%w40_UWq{5=XU<#vFzxE9meUhf_~r!=0+|pp-}7DGu81J%vz12FKZ@N9ROliYUnqU<<FB#0yBVBwlokN<Kz}RyRS4;;d+Q@HlGSEW}ceC?=>?Hxz2?8%v>f?s5;A1E1F1a|$W*|NOY!w@?(XkO}-mffS0Vr~Nb(6Y4oSinX~Y{@K*)a25mQZ|pMejnQqtPEf=kguA?5MMBC?bDjBC_(e@(SmvWDP~6HM;A=w`M#G>hj+S5(4p7Ouhh?;hsE5c&vNJ@3ftIr@T3^jX%b|9^%0o+Kr^%(=#?KhbTBTae9Lq#PsDO=Y!Y|<n)gH8vb5zK-G@{G%WFL{`(<HjSY2yi@H;zap)i5gKOR|bc^?4}m3Ml+E6BH@fI^(w=e5Pa<Z1;Zf8QayGOXC9?_XL!JnC=@Zw$Gu{#=OM^*mv9yg&q3r_Lt?JSKc3beV1HOgapI9ebH?BfJ6sxHbac%U7A-!t0kOOpFfVmaFgLTLbe<=oHOh_X(X)}mKg$VBX3zg`RzX{+{9*otf?g}eHQ9Q8YYbJEj14_^&|VSBDGMfb$ZLdEQ@4&{_WpE{SY+<ihDrb4~fRW)A&AhPc)UQu%(_z%4YtpdE>|@A#V;%-{`2Q)F_oow)Vuxl82P_-cQC_xiwd-5{{zeohjzPo<fN1{ES`&%0<F@A|*j$OR1LgMoOtMuJn$T7>Hv8(qrafkS4>r(xm2LfD##$1Hb2@lSv*Lvk5VncCuJ@JyGb^=PGmw&*FHXFR-rRKbv+Gr{-w*8ZP`8FjL#!n2Si_F`tQrJX4&713$%CiX_fFl1OgV@!<z43lc^mmEsjin)wJByfO<Rdc12UHdkK9i0zVyIcH&X_M-{yHfZ{gi?ogl9xk<H3$u|)4!h{&sZBTEB}R3%M@?@Nr(=oB$#4Ieao6j_-`YUOI>CY^emahqLo0)yl0DPr5;Ke=x(JrHf1RM1v7!FMS*#Lt{$Q3WLh1LrP!S5h$7M=y|M#{?5fby4sLeYqQBK|x<&<V%@_rX6Cwqa)#bBZ3Y4fhjlQUy^nv2r=U!0u0#VHq;54AKoxl2<nDj#lPa^@~f3nMjiS=xGsWyzVnED?f$-^+&|=yLQ%g*7G<JPDwasAlZO-YRSQqv=pfVIQ+k#=T(e+=FQVDHPP;!(5Zbi{-m9#<(axIX!K)&l;Z{oi_F`c!d7Dg5`V>JJGw2@dEm+e74QLq+8}ZCO5TF8De-f?;5-B1B8(~p1Q*$NSxxi?qk^VqTShl<6)Xni|*|wfipdIv3nHsyloQ`Op@=xc3<OzGvW(sLC}ym96_+#Gn!P00suW7!*N=e|L})K3HcBtzV7L5t1SA-5hHdd%)~c9t>=a^%&9ox+-9epS6(-+xKZR^sP`(97#w&lNS+1xT{_oy&^r+R6s)jw+x+bTE9hJ*73Np_4Ww=uspH_yn;{Quh%0OoCKE&KCJPT2TxJkWsUc8JCl&WikVYQq0wKTT0TcuY@z^x>$7j;lmtHKc_z{1(SXLLMq)TuKnKvg-#9I*Ue>bm~$cLdeTQnH0?+%A(QcT*l=7e1U;JtV$dWKHCbGn5^bl6$x1X6MhrW`;&=#<t~p35%zQ}M<Q@c<A{Jwc~Mw(7QPZO15wE_N-qqqYnnFG2FiAMA%*V)L`Y%gLv{cZH&tT;!l=5~W3^VGVwCOkagV9Ivk&-hfh(h&CDxf~y1J<wk~cN=2`>en|YTl_mGd-D!M=E=E-|t#R$6qskkF6yo%TaJb>ElMmMC0s1u7D)(2DGz|aeP9h58s3GQ$&Vb{|eKA3d2lAuPxN6P-W#a=x_Bhf~{fGh!Bb5<^2DvkhZn*D}k&ONpqezocXOy7$gXiO<$>BPc|Gj2=Z~vh2$q|-1ZyYxT6Ji+AZF)_8RYuFg=ii^!vJxF5k?vHVd)$RTNgo7JM(PmwO2t&ffWk>66y9Gw=m~!)SBqWp;-!=rc;ZCMVZ!yHrzNSQYZcfr4vVl?FoQJq{4U05!T=#JXf+|J{Spa<X%%m5yo}-wr?}o=trr06CB349QEU4k;P645BnRY$fWUtPL~Q+`9t;K#G;lDB1h}LkvEYeR?2Txu9AOz+5s`$dO0OmIlOSoTqY5lvo%Q}kFnaVXR5M2ZUn&9X5CO+E2$vtK^)OAOqto5S(SFmW6JOi;>Mj<kNf^WdI%ih~ZghGDG8^Ani*G7`*RY7-Rs|-dlB5Mujwfo5pIB5tawp9vF{o0+N(!l0<g*AT@P&bi2(8lpOWyl6w~-`?WAFMDE$sbv&>{c<;2%-sP!klXf4drrL2^c;;qo{QpaHZ5pt0Qz640z1_Bq0j_JbWhhvOpb2tWAg!e={vK8O8w`+gr{KY>4j^G{WERdqE0N;7-s@Wzga?#{}p%F4>h%F4=Y^hsu_z}nRhT3qdifB5+_sDHe|f135j*H;hz@abU#?{NVb#@B9u0Mm-*%%(*@1W};JwbLRf1sT+g*=(R-BL#&ct3Iqcs`MXP6-}d1PjDh>_wa8Wh5tr0n9E@2s6`yJi(l@`{#L4ujc<I69Ihv`=5GWF`>HAWid7$8HXdwz^S6KV^QWr+r^`QF{oxN+4+k}`@`peC&2KAuI$^)@9%gd2qQ8`pk;XyRg<ZfTyoLSM;Msgyt^6&9pO=K$@G5^(@oU`RJ^oYkq?ezXd7t*3q30>Mok$&oso>Dbv&a*6d_QUv4Hy+_&~qc4hux}RU_HR%eF0t!_DD0D-4G=zev|<Gj>iI;`Yh-U^8v=!H7~-^Qb_oR;1dK8q!mrLj5b<V#FVlIL1w*LBX=_QN68>1P0%qEmD^D@oZy~Hl1LU)GmZ7xDJip4)cTbi3MYOMFFGC#La8{j2n76Ll7jG;mFU<l1wEIUOnj@PSKLz+g#z-y&)m-QEKUHdfr=4`lWGNHj?_`VsgDGTN=+9&KwG?m)rHOewJ&v5SgFHF59lSUJq!OhLx;`-Ph#P$%ddLK&voSQ>c+;%gg(bV6Pvlv^X?*k39D-LXK_(x7NPPdBDAN_KHkaXt*ohPuM@_7jrS<rjr;`iptSk8Lg-u*z}9tff%}-lNl%TUuSXLjf7f7^4P$iK#74o+<hxgxN(ZV)y&wsJiv}=g=+n9H(Wxm+Y23Aqgrr0#M^thdqwrCqjU|R~1_bO^8cpb~0D6Wdfb%wqKxP2%vJ<JKfk>j#FgB1;*9cKoSWRUM&kL|sb8Q9I3{sL6k^?Kpu#v;8-n6r$1Kk1oEz$Es`bZRnfve=Mx+l=_%AR;bexOJSwTnZWb%-`GCPt&tsO0xM8Pcm9c9ICuK?mt#GGD;uFbjC-4Z|#xcl6^?PxIH*i<W_Um96c6`6my92Ay+a7lh<@91ERtW#l;j@(+K9-fgg1{}Cba@kg&aLtB&f?VbGgPJU}*;unn6<>M!MGF>q%|Ih#MU;Z!Rs;3sFXQ#RQ<BwkT&;MP!-Dv;$?;qi<ygdQT-{b`-QPc#@1LGO%2COc)YUoOXQ1M{mh|#~KH&b4Uu7qkSl|Wsox(!AjLd>|?i@TJGsew6?vhV^3_m;j@)fc=-SMyF_TJV;xasKkn+v|&GKV0~EbleGi=BL{s`oL7H6S97Yni>;O>kviN_w7{<?~6}plEe1~KRp|TShpd81RN-R{HxI&#VKkNm9(2g)2x<ei&0pkd0ay^5}<+_yKvVoF~nazYVA(0YQGU%*7_icdbQt>Yihj{OeVlxep#sGB)FALMBGO#1V95wB9VO+AR72o^=rAND+fk^k<Kc9>zxzYZ6i`zsP7ODA~Vf|OilQ&tY}aCt$_fF26(2lCu_m*3$Q_$?@{~6C%a0StZy3;Y#rur`c(nxW4mX43)Tg=A$|xOhHvURig7@ACyR5Uf1DhG?p?X0dq!8aOH$m1G@;=MCPM)0Tqhh|Rs5m?5{`0~(Ix~aW(m%S%L-w|8LOei#~g3vs;CT0QlU;XYJggD2neIjEDNiM+Bd^)-k0FMBSNgTy^(`1i_oac2NUgQ415S1F>K%-{kx0><gZV5ylaO-l!@v>UTMC2rPddh?pkc3J*#<dSE8V?zNrSlP}cB^L%Zb<G%!+K#krX3!<NI;^nIkqNg1_L+6-12F;5eW5{xb15N~-x<m_z{4VdQX;xx#H)wuJ%Mh6Mzstl5f0*Oy4L@H^^l}1IAo81{oVJKZ5i=J?Zsb+-%N5T*W){xY8Rv87945Mn`-%G-F8C_jDlyLZ7WQ?@f#~Ruqe%+3Gb+6^_Y~BN9IzX8UDk<=#`JJ*1$FyKpeCykRG99d>PX57eA>p~<Ijw9bJ<#OOC&4rw#=7d7Z)rfKo8YO+3s}5nNvI|oi5b1LZ{zBP;q+(}Pr@qCD>kgTwm0#39A#@(!lR$>Wqx=5=A^-Da@1c`O<<&{1z@zrHxhY;4P_}~8D=2U=eG^5!Vzyb{Q@fT=dG&p{8<^`RCYH{#S@=RVf_!09#3akM%uHnWVwgTq$#!^F-X8_2h)BETd28Zv^%Ya%_yR6A3wkMtNLEjbE|7%0__?jl*uUWc9|?=x4`PM$sKwTVHQ3p*p&-JjHgwzXl~s#HixCdoGvC^6!=LzN}nh3m<~6q${tFW;?BDvG?&c4vQ&2%;>{D>^&Y}PwfGn=p&p)*x~ON5jf;Av4D;F4)5hc9CG~!VBki4reiQI**ugWQw)g7v$a@N!KJ37&KiyKUrUsf<euBNReC`gRTOoQ!+&~%nGKFS;8>T7j+<)?ag$CnN(V=G1b>DN=MTmg=;&Z@M!#m4~8Y!Lg(7+8n;ocd%C)Pvm9;;qTDX1ttLDj~EG~!S$2OS5!ZD>Scq_QbFPCSt+pk(?YQYXQSwVB`VR<GSTTc1&etZA?q#X;|j=tf37Z5{hE8s>YHk`k)T1q*iG|2#{@Uugsitu8Nnm-Z_QXP6}B_97mI4R{$R)e7=|KG%6dd3s|BZV#PplEil?y=83Tl3p64=yTKOT&wsyo@M4IuF;ywpi@iWJc+8NIcc`mJbxh@T?HmR53M+zEm<_|^N5<)+HE>kF;2XRmA;z1Cu=5I2iKP>ni?)m04|XGf=6KQgg1d;-_|=v!;P9;`GTa+EoFsyI>-+YOHk#uEBQm%lY9h~=Yij&3BOvY*U8r282}?g^C}fzSaA&F6IJYJA`5C9(|W7s4aDCL{nZgrd6*YLa+qP}Xd=vSDn+ZrFr2e33BcI`)3O^R661t(J&p0Ec?6fxUMxw&SCb4uFPm4er{y2O0Xs$toPiD8lEAGZaK{F2OW?K*{E0W-R%@Recst7*o13XH>)?vU3gC9l+wxa7Rse6+pb2(k?-`A@$7QTWh0eID50gPB_~sAQKco+;f9P%a@VDmr{V=k|ZM>xKV<vdByu)Lra<jab<I7DO;*(=pNGLfIiv5B5)lt9hN9jp$QcZmAVW2;B{37d)W@F0Y)NZvge<OzdXf__TwlUA+fF7EU+W62Z2!Aa4#A|JCJ6zF97KQxS%bJv*EEQ?eV<|3IAQ;8tAPZ#sDYsiX;Nis&`?k0f?|IJhwpW|Dx{&e&CfXp=h^X3BFZA|XWUy2B<R`m;HJ7gVq?<O(PYwLZ-&I>BdWBKJQJ>I{=b9FcifL{^FtXj@z?&zU{<70iS<W|Y=#jp#kU67d$<ZaJS%?~fjmIa=g;PuWN6ivGj%Jnn_X=`J;WGRofuPn0;>7Z56tqhN!;jLjFjuqmw+Duy%C1B~S#Frd*P4#dcQwQG?L%mnyQ1U0+PB&bGo2y@8LYzVwZ!l+ELNoXD2iJ20;M$P9kNAov29*X@v^;jj-f!}B}dXc!!Zh`=)?<9Q#JF|vhB6nU_T9eFTxm|$rpuh#mzV6e?AI8-3%^b{%rYT?Cbf#iZa1E+&ASy$vM4XAIG6T$s>0uo%*oHKAd=<N{^xtPtqA}A83MU)KiakDr1aPGl?^D!t)|v338svyzVfD#l2x*Lx-Lss?dw!pG3o#&XSwxCIp;WH1gtE;>EWU@9^mN4Qr8$(537wgt5-m(6UYobrK_HXX)E08&=(J81_+<RtJ!@kbBLn?S_0Aaqb#v46FBhIC@Fg%jt~>g=i}vfaTX&z)_X&hUA&KzjRGo#y&bDtl<cv^5Hq#0(4umJJ4~aa0y|3v8FrG<xMFgiQZtH25XOM$#8v5&b@hUvVckT^=tB-_=L1AfbW-iIjztG?(FhpDIFzlPnI{AthVNvB5^IjM;q)kN-=ciYy`@H7=nZhruOlMVM@)x%yS1VG9{j?-l;jf+FUcDo@&k1ICb!fhZBVZqR(61mKu!LUAkP$Q>k@Wy53))TShfYsuerx7`kD8#=r_~!64<@n#f)BkR?m~dK^eQ7s-FRStw)Yd|{q{I!hN8RV6Z;S=VIO6%1=DSYzH%8P%wf(*SC$v&SC_m`r*UPcbJGP|&`_#4UW1*iIDmde1Nm(Q9<6n}Ecxhz5e7$?b6Ajj8N}H^?dBO`}J<#^Q!je%imM8`^$B+pFE~QUmOI#aDOxvpR13JPSXNWbqVQg-06>OD9%i9fG))u+>KOc(U3!T|8~kZO)z>U$xL}O<U6qwbDSFApS~CTnOZ8M>hdAFPwb;`B$~huOh(bc1QPE6ysghX2Jc!2x}5e+QCJ+nzx%<u3Votn@!)67r(+$;-dz}G^hC26i+=&FnuuHJgZSa#G0pNE2xPO_V}#b=H;-|zmKwC<M=QalH|CFmzv1Wu4;M6D+M7=^Ser(H%Z3&BSl-zAEVw}f8<E+`ST53qu$FiMT3O-eovd=^P0D)c^_-u1b$86=LCL39mnCIXf}*cIN<iK!FV?|a*m|e&~!c)7ifL!JM@LW=e5}&P&b2!MidN?k#d##q;={diS%v-HLp|ix_TD~JCKX9O8^(Hw?ssZMlI+K{Pz+5o44UN{P(e4z>TyQy>}OI%tCV&1<i(IIm_^2)gjPn2z2U2$q)4JJ9rL8eTr)d12xOS1f%EAQq#!`?ab{)(|h0n3d~Io<<a)P;NS0zds|%qCaB?D!oWXu9Xq_zp3F;MX}6Hiy@RG>z_3M4=xWYo9oQURknMRJ8&~f@jd@mbM5a62sII~$il9zkp)*%l-?E(;DWWKO<!j`rtKaGtmGWl$z}{>h0COAu=<aLk2x~4o){WCD*Kqmas*n&qSxC4vnk<3q(S;luiU(MzPD6pe=jKM4a0Q(dcFZ7xpJ0b~&9exxVxI+Abv0QKEr)X-a3*tpSb$Fa5bNA8luJc9(G&vCTSJH(Wl596lGLDWT<HkW6Ffl^FX;Q%Jj%WrY<ydG#$g-`C@!LsHN4m9IR6Z$XmmK7!1iXA9tG2CHy+iz<kjRfOMj3*V4@^%W*JPp?}HKULNI*wcT;nk;I3JelWv>(*N^1p!3Di<FxsO>aRZw=R5W?jqb(XN{;ww4W}9~?6Jv_O<XH;ka<ZIQUX_Z`ap*4IzPX0U@BnXnJ@j%F3>$M9p|c|p1@+1AtD=MOR?&ujGhv$af0X(#a}~>Sdu>EOPpDC!5k6B{z7_oMFGK$6jvaoF-Hkv@w0!SBc!siR4=NX;*1~#FmBgs!-BCZ^o71zr%zOCBFSR0$lgH&4R0CGkDywoe^i#>^i{}Fd5*>x-SvbY?3Sv%>xQ5Ya@?w;RgOo7e28rQJqa@D976^imO&^AX#jLL43vt&h@-ZSd7(QvO0hA7K0*dB1CYXy!5Q%$Y6sHBj8bDn`qT@9RLv-i6|EA6RavAJOs={wUS?mUV;2$aTeU7WOF0R%JT>5V9BZ#B}C<4;>qaly_qiAYS6(RS$`|#&8sA|qWouD)Up{|n2M-;3fA(5GZ24yo&0=6VzwB9_k$~D)hAS$$E`II^(cTqG!y$w5Jy-|yeT3?>V`0qtL1=TDbg`^qtPYgL_EjW}mO4pY*YvMQXUu#!G;r$85-Iy-psCSmDPS6BQQ3`D^Cm!WedI^e;28trOj*T|)1@og}ob&`Rq1ObtRJb0BR{QX=*?82}Q4AAP_uJKa!<9=q)by6sRoFMx0JE!D>KvF2)mVeOQKMrWSyrsIP#l}PbUXoIDtdxq<Vl{3jt{<u&=4MRdZx<{D2Ngynw;rEB+=aEg)$yz6fO#{jMnh!DOp+YA&aNlCwP*dObpp<@|0RhP_qeUwPGk+txdVhDRf!V5T0DxZSdOYb&9=KMQqL0)P!F{w|l12`&yfObhUyzQryuXmytREDCUT!rj2P$^0R(2NFh)#*$QIgOfnJP0Q9=F;vrk3Fq&fM58TX06BK+_4?3?VYD**-y*IbJ*(D(Hnf}nEK@I)Yq(Bqcs}OvLAn;$c;nAV#<cndSkQ(Gt<Oz}56A>zNR|HenFDT=L5|?RGy<g!`6Vlz6)X(&G<iQ!lS2b;i?EixyRH(Q{e&H@Oe<|s*fm8kg4c%ygZ~1YtUnuf4FG3Z{Lik?3C=|P;ny|hHJl*P4%>$ZcHSczjf2Mi2AwDB)5!X`!eyZbos^Q8%D_l<%uG|#IvzK@FY7K{mQgfvIXH6G93Y+>s@nkQQeM;4@C@W+`dBwEkaA8N;rS&?B+5t##%GayCc}~6FLXfJkvz;t*U_na)#)5jQNQ|wZq%;jR?JkknTR{zX;ZI*6CP@KGr2^y<kV?@IoN}2eDNm}2_?ecdCsrx?{a(l5E+)8xit%XcKkrcLeZCBp7o&mWQZx+u&-Dwv=b!j?4IPXQB+-Jqd5q>=^v$cn5MuzU8s1&+4slzbT9J#O0jO)+rdC~tzzsB&X9GONCIdYg5jQ9y(jNcj_+@%YykLLSFDXBjg{Q8P==j+%63!Sqp#YP9rO!vf<O3NUQj8(E4aj!I%oJ#XG(6(qTDbB^3bl{L%L0LP#QH8=5DT*>6s&hjgPS(Way%d^b`bT82=fLqep>e0Dt_LbTTNJe6<<%Ifk7Mcr;Fl*ZWYlDR~nG({J0i_*i}?J+Ihr2L2pHdR$EYk^88lOoY`t@`aZxan067S-Dvwtl!|TI>+lBlFq%#$-isdSU+CJbMzLHN2`nu9bUTegBjln+e!pPy%=dc-7O||YpHfTEEfds23)q7Cs0Mn&LrYK<Ex)X3@yO)`jDF~*f2$wb5El-j4IG_2P{P_wehyiTx~oOf_%tIvqg$Wu*>*=+mBTEF!=j;TP&i&=4+v`T55oQ;?2I3M8{l0LpxiR|(P<pe+6jAWbIUSKu{`B^ySR<eb7U|I&w^g{Bb~eqKt^WW;WgVoNTQI;?Sxr?iNO$p6UE`FZcU%deqmR3s_#yqV&0XV>Khb%YnDqBGzO^=Ds+IX|45+cqd3S7w)W<ZjQ`8P6g}TFJ>MfeGx%$=Rx*b*5icAi-Nqcveyl#7!d${v3-Jp3r5%YaiiN1>8%80-Q}E|N9$~{&e*8duAzm&F-xt`2ak^?c2I9PdoCXt<K=Q6EoMXaVk+jhJttXZX;k<-8R4mfNn(=K$XHac!9=AC54*VE7P3-oFMNMPHs{zKk*Rp|H3JACdW@H@|Wj2JFkiCyOIy?xe<&&ayh2~WG)V#9F+7sw*EF%<DGzC=OL(3)^bp);CnJuK>Pb5?c0L62bOmX>sf(_3fr-d+t*+Rg-GvVKrz|S=Ntt;e9g};f91$Yg=4*yQU>o$Tn!rIBK1|=`9DQwdme$1wZWr8*~86AXvG;J2Vi^=A$Pk5ez<?!PSkM0P=tYAWzybdRlABKx*oM}hh-(x6_KmEy5_H8=epL-7vsMtO>ApcD@%Ex;~YxroKECx-}(D0E}hfOpHFov(`aBj=AIw%Be_gB_FGD4yXSm)N_dUker+&+Hx!evN^=zPL3Z7YsJQ>$W!E6c@z4u`A*eu-8S2rP-97DE)d1%e|CiFRCJBCYZ9gz*w*#?}63O~7SSOSeKxJM~1Ep(o`A>-P$z%wjF2@;Rx>bggxghdic8+9{<!#%=L9f+Z9~<iVygL%({G+#*VEs!L-)p!DZUxfke<V%S3gjnM$SjiEJ(+*g)>z7@ObTijOXm{dTV+q5`3q$T9Am$&Ivxrj`oUu%TW<wG!UYH)9wv#<7fVt&WRkEJ7Y7L84VWi+8&&6v+pod4*m*?G_pv53B?U~&gtqirO8X(8lY+v6IgzQpT$s6}D=RdZh!OocgpXKO#_oeXs_v7{S3;RQhXgC_CJ$Ab>D*JvSZtC-0d`!XAW7LY(&f0C{KN#D~FcG2RCn9nB-@4^HGLb9OKlnLI8av#;_YVmQDEI*N7dE8#m1tzQD?!;((IL|^g3nuL<DQGoT?zG9S&UOviIcHcdVjiGF&-EikPn{E62mQ!p#S?ntec2hkRmG=Yc%qe^*E`O^-#gFFO>w!R*d#wnH;NSw6xYDx@)#&7rm8Gy^(U7frgNSMVboNDhJJ}zCeBZc5H3rQ2x%=b<&O$or$+vzel8j)tCSQ5LSUr;UKCg$fDri1G$ZZg=&?4-?t~e#r2PsD=awL0VXG;$H7UD_)~f^o-pu&IC8AWO9i_}@ZJ;*g4n_dpNKRs+CCW`vaUqwOkCAtckGVaGQ%a%jPXbs;ro25q@xkMj-Q0pjYMZ3=F;)a^C30idQq0T2XQkf97*}z+3YQ#lXTACpMOo!lhsJN7<OlM~HobltXY#dD6)6e=y*=VlC=g2{Q%>R<CLXekTf-p5R8I%MEio<-icXkZDx6@3`5s-2%E#e}K583;(>&fyMSi3rQjwhLv+yR|PSIe^(x*{kLuV12cQ$Q4u`+p)Z7@e>)UA4y_wJWyK{0<;p%FPJJP!j5F2@JQI*W)8e7tNjiTK1mawbl8&J?}L#kpRDzwKLL(&wD_%8(UXq`b5Z+nMy3oazi}_gu`fn!;<`uCbs=gweDGm6$G$mjZy6JgoRO(eMN;oUT;^tJ!y|<f#Z7I5muwg3iFSZX&}6WdOBWyJ4`Z%DAI@66s<?E6yOg@X#8W3oiahqCA_y?~(WB%uC}@)blv`G9HnCxR(<v32l|G!@ah&FCp-4FADD13Ru_XP{5QJxyf6KT%4qmEQ~0!m<>+`gxn{p1dQw{w93q3cR87({X#vKm{aKc!USKq!AGW%Ap=c1TNJGeawR7t9iBd=xe8BzII`=WSFLBDh-Y)3D0p=ARxbX|V_|6RLuf;dO(xJ)e9}(6@r2Lxc~f1dlTFdDt6I)w*4eFw3{MW%L?-#U1lgz0W|H@-hCDyc<-XTsyTy;PLsAo*&V8N7qh5*Evmk|{LrsYXgB(J;`)o}4DCtV4rA>>iCeKqfSiHZ`+M>A~SeAU226oB3ZrxGBvcj(=9F*Fa{ThPA;ec9Tl%&YaN}NA1JyY%X?4Y`ek{)&MORHE;^1sG3>XJK0BIi)DYz}qFZzSP)Q<DTJwa0uPCK;VjU^+;ajDe=@z*>bmBJ@q@YJ6qA=l$sLme$r>kk{g_hGuMC;+m}{7i_*XJlcLo$Nog=MxV-?fs9?}9f#czS_sJYmxx}4l&?h{$-u}wZi4<XK-3I_Su!TVWO#@E(B4#QlGY<bcxZdg-h$F+P{`%%HVh~EaG(WB>cM;7IjR>mj3OvT2ZN}4R$fkhcbZOv$r*2^4)h(V#BUhMs9UFWV_Y**<zXi!;5^mO{C2iX2~zVGOTYiR5@s%}=Fn_&y5}H^B8chzZr=I!eg>p_9xe?F_zRsAhKo<yW<ctiT2|IPsV1hfWtO6={Mwj2@iujjNFktMc*!ABF#+wL_X|L{9X3X_00lL_ELc+W{e*NxmaVsQ?)vt59aJiJO54)a0qbzU<+}z^N*&?|Zo|%@l$Knl#Po`VnhMfN&A(`=CX(rfoX^EzSe91LdQnPrm@iez+3sk`Dje(&iA}Jvn6#4|q7jc?t?D=danJdu>^i&h%U-NQ!_}y$Gj}4T*@{ky<XjtzgPK-za&q!qGU=J$Em%ecfKp_@-$Vz8Y4OYO6fB<F4tc5YvGPPaMbJ(`1mQYTltDZDMJR_5vcP`Xna(ZyqNy%Xl+ShN%@<ww%7fZUY~~B(LG{MWBCP!^j$58zd^MP6`4X@N#?A*wBffaKigE&si6<XEi@Ddpw2ZwCW_4YD{$&~LuDx4|qu8%|Mjn%Rq{o?m9%c0l3?KIUD8sN0rx?Ww^r$?t!|$Sj_cTaxI<~#jXabdO*DvVklCO}!i>*4{sUgG1i(obg{eoLDR0LIU33M*DJWx%S;?MUN{&*3FWbGU@GW=znfnXmGbZ1+`JGkcUTE`s#bOs$gR`*y`QLXj{o+=l->adm87c+A!P*U7OQmWFH;R?KqPvVGKHbk8Ukmm_^^=sHh6w-!KtZO4F%2Y8GzcBlbdJ|B`vj4s5yf1OQW)#x<nxFK+@TjnUdgE2dYqwJTt_c-vu^>zlj^c>pjV1=vJaGs{I|0#i1*q@lVTKc=u$p-lvaVLFOr1_Yc_M=4Rjo~C!{2lbm-%culIL~j5qfgclsk<_K_YXa7M!?uiYIoH--o6}AARMBaSX5z=NN|(4UM|{36*{5nFl)`p3z+<QDQ^XfWAO_2gw|bV&ia9GMVL7Lj7<~Y`T)}=`bodaKq~}?WJ+&kXu6+4-cq?&U=S(A6@Uwwr$w=5Scp5oDpDX8q;B<ylkw4d2YT4snRDOZ7yJ%Q?NS>gr7l5l=>XWLoIZiQfG@O7R<S#fypD<{KzXW3}PJ5e-uMd?R-HLc*6kPYHXWMEzpVQQ9{8cxtEvCE9?8~K>sXgp=E{2Pcx1%MWJ+W1%{ha@-)6_dK+S@f(;KQHJzdBb;P3u4&Dz129aOhIlsJ0<<d~#Ak7?LG}tl<sG3DU8yG;`*6VwI?sasPZ(~)XoQ22=;4UQED_BGqB>Lr)?g!kB(5>CweftY&G3c1d>|OV&a(L=$AZ?G|{Fc^1j@-JZr90k8j2n1k>tSAm-10>e_TA*u7}fHhDWhGng!HT_C!9kOl5V3hnG5n(m4qX4-)X_yEFijCTeg#bTIyDv!@OO2Rp9L}bXS0GObBOc@+~c{@=LD`0Q4_<b71PYH!xj(Yv9&>D*%VjhFq+MbUIfdL_v&GFy5S<P&yl4Ot<3tfMOuw`HyR%Vq9@SV5<8u-7cI3fessX!R~aaBbBQO%W8UOeE;OQpYT>(P`EWND7+On6mA!5xCMU+FS@T2eC7Zaob_qOOMiVTvcj3p1*5$7-&$__Z&&*5zqK6q-<EmquY1<)_6C1zxP!md{lV2Ka$TGtmmJqhK~``Fzmqrkorh`#`Ez&eym_jh>Um<kASd%Bj^Cx2R6)nf@{=ysoM0zJ_m-uX#s>O?KNOze-C&wpaW|aDqdME?pw3g*A}CZsCyHgTH37kvnsw088R$}U0I?L^y}R&)QZk-e?!C;?O^v~S;3sP_fT9=9qQV(dFQ31%os}t|fu<9in#xn?c(ibX2-W0i0prCoj2DFQVj0E@+vFAqJ3_vXc~9|F^ywq-3L8O1upBPHLnE#Ty_MwzciK`$ZyRnrjTh-q7@_L;sZNi&kP&QrXPm5z6p+du3XZqXMi_x1!Uzo1B&R=voC$7O+B9UTcv^;xW=f$M7c{W47cP$sIfLBID6p-`$t7q%ea56)CWbZ9nX^Vs8&d7}M4wH|i%rA>eQ=l4#<!*q*~ENYw=6zPY)mC(<$%_VF*2U+R(7Huxfv@BwJuZY@1nusq(|0PG(v@`GzXccR6M~ZZJo^?*F6yy$O?z>E1Np+YUU(!MB4~_l`xvz^6^Ec-Q+YdBJvRS4R0H5Adef{rtdtc&UmK1X@;Q$n!pJDD6WRTME6f@1-e3S=T?qZ!)w<O`5Br&!=87ZA(h6Sw5w|v-$#R^)t14@A>E^H8(U8p)ZPywTowL)x7^NgKv<T9yR0*vrIBvKQ^Cn(08A{OCjjXEAVVc!u>j+wom&17`aYeSD0cOymQzFy_vy2n|Cz0?{|e0)gLaOW#;K;FouT8t5_JxXb5{1rP|sL_WcJZL`J9WC;WSt*L(J@0N<^^^F3Tm2?PjGPmzgil-B-(%moU&y?%K|41#e&|ey^}WBT7rJUhy!!s_|ZoMo<6vPIvgd%NDGo_DDJ%MSXH6(y!*~%~!TIGBHG}5b{{9-9D!}ldX@UjB!5Qb>!cdjBnlm^5c~^i#zfzn0;xi1U@t1qcV8*aTGM91zeJ|tN{BGN{XqU@2?8}cZa>6*Y<9tTO_O`DSAX!>%qe|5{`WEsvGi&Vm&k)J7c^@Je5%%%%$jvmUp^DETx#dz7m+Wa2e%s*IFH>B6#CeMChJ6PEe*ex$@dBryuMX9*$78(n-%1p;mosmwmIgFv0Z5;>GElI8H3b%e<X~>DhX<Bu7YMmXO-D89X1srJOuYiWVs?#MyLN7)UFgG{u2*-e~BiRycIrtxc@Z=ei?u^D@0EP=^+?h=SavHTg50s0oX2@zJ^kkhJcEOlm{o+Mhy7x2SZq?J~5A<^s3&tW|(09|;it#nn7AtHH7U;);rl^yxFl+>B{w4YnypXb?-o__|?LB;RxiY|DUcFU2ch+Y)vOUYwCNNpJCEiG{4)FuX;Mf>G2-0@~bQ#=t52kFd!5zJ3zpb@^|D<U?pgO&B218oF|aW5;Q35MnE%r99|3?wL*iw&HvCC)0@`x5^#sa-wbQZ(6j$={PUCnrEwc#)2w5Bi!(Ia2sL9;eD&NX99Y|-jpEJu~L8~sx1@M0CzLnX2D)K$^yB3G`FRRL;P$tua<=R-Ey9`cS%qCK$nrXebr`D(#|m^E<n~ri&ej%AdW=S`v#*8Y>RunR^c-)yirnklL8jF%OYt`V@gBlx)e<}qD>;U&~JGYR%9lXo^L{+JQ1UZcx8;RLR{kF3N$?NIryaWlckr&(=rSgU2+`^v&qvk4715a35I3iJWuWt@A%})BOPZ?V=VJ((#NEY3oG#NoL%;Id<mC(I>2+ytIjd9YIjcgHs*ezG>7k5QvCIj;)@lP^Ynz0i(*Mtv3|rSl*M$`$v|X&U!Rab9Fst-0!2Y=_LCUnP`&fWX97ov&K{ykFPy_n*l770KBV8`Ih8ozY%RydY$cuf1!okcxm6YL)M_h=v&Io)=7=$Q;J{y#Beb1xEaV&`AFHYV!Ka{)yZeqpXtg>~=KM}t6-}%QbiP?gM1Y1OU!yt#(ns`R0~iutQ0^7@&Jorh>!m+wzukkV(?dT_wHSLimz`8HVV=?&Ib7(1Vu3I1S<z92sSO;;xkGn9#q+|5dHj-<9l0*Dx+8NLm2B=fShA~NhbmiA5XI248V4^+?#iK%T2^CuK@eLj`dCLA)qBMYtti)4wYE^$3U)>pujd}!CdV6WsdqaJlaL~$4>8elO4>^}=jfEyaFW)p1vM^6!Ql186qb`RX*n^)<%Hy=xhZ%(aY)RQB_eZTh^-Tw<xgy>Iq{1a47uq>@p>7G#p*`n($iJiDL-?0cd}C8omdj@L{vqyZ}RU(=$+hE>YaR!*mKd}B#SFPoh0XpF1=2efH=WVgaD&gi$a9|D1A21@M?{BpfxAIcG<x=fHa0a^|47Qu(Z!7_II?{>8Lui&N3sR+V~g|U^(-xT}&#YMs29I&R@G*GCwgsy76r~@SQEgr#@QjujuAVbr5o31j2w~Hsr_$M61qX-vMvgKEsSl6&+BN=T&pr5)zW3G9*i7NT$lLV5`({wH&xkh<QE-TYCvMl>2u?x4CrXS{Ip)0r$|i0C5Wo-fep|7;HdpH=Pl#K1WA?U%D>Yl?x?<cPc7gzG)d)R_0}1=KZoVLba$#RYCl?Lm3%ge?=KqC~8tW5I^ovMh4d}HFv1nyzisIo-mu#80ntEU8AF>J^HuCS_Ee2dAr9ue(lxqo>&1t?f;7DU3VLJ+55%oHeLt%J_>IsBlfe&00U-K&!R!ptJD4QR}(%-?s*qUFiC;!#>hxe>Uo@WVY9-wgMN(!ugKklk(O_r4i-|;ZtZFZt<hmRJWb+(1&;AL9j`lK@9C`HC--^lJ%%yhL{T`e#Cur9UIV5=8DVLe&Q61b?zjKUm$#)UdK@NrG|%&K5!~+Kk?W&2-@zk823jq)cld=owcqnv+uQPPUlt^TFx&GkrKzUo?KGNK_vAfs<ux!4vaMIWaFT)QS2f)O#x9rHmNagUFPo?}w?MPG+*ZF@`OB7gtF!yK=(d0j_;xnRqUmTsiD1n}#L8{V-3%qs_}&c2H2gt!C-_mcJauq6>Rckw18)nZPD_75UVQMfZM|&c%T4R$=9QMAQK6(42VQ{md4Tn8!0#>k-J;*S0P+B<z=u|wzHB-$QCkR8OT)CSVR~#}+FXXI&6wI6rX3AaiyJF2Z7svJ$(S}ZOpkO-EgjRgj>*U_3P|0|KoSG*FrCGiHTy?#z6$?g*w;8a%R@jo(g+FwE0>^nyKix~$@~UiclYt<7XGZK#Lh&)Y%ZZ_Xi|dO&I`1NI&v2^CQ`!l$8~1GX_%x_5RB1HSnbC*i!&7Z0llih3<xORPh$2RFD+r*)rZ_y5Cp=_LLe}`LvrXU;sYfQ5$@k%x*;nNefqLWG;7O7YU(Ef5?%WFGYf|*)QKneA@=0~G)e;?qUI4~=^at9%BF2B`k+vB6-T{};}3_~kKawJ;UcVwOJ0(WC_DOdb@vN<SN8ypVtn=&`G=PLfC8fbG5^q(AKF)D>PJ&m?#~e)7B!XSKE)jGkM^-P`Rk+jl?M%+O@H8<jWziBF8}!>kLi9f5Div@0mvUe#(c%16oQIUc(+cfBcu}|75WrOoet~zAL-}2JP2Wm<PfiaK!`a5YY>#BmtVg_2uAmV;g4hyCI!NzK$z4bOiF}FfgI^V{rV_=>GyRgnth5j_0jDy#Rm2ldX*Hvp5Nn6DxDLo0f7zY_qdT{Y;&U;o*OQip=L!o-{&V{+H@hFP~v0#;*mv3y-L+Ft6`3ag?MVw(?{{tzS1h8`7x7~(EOUoN*+@sGgZkZS28mynHiPLoRx6vp!4*!!%vHSZ3@?ccKYP(8+G)JI{Jk=mQB}gJf21)QofR4Tpf&#Q2O7b=Sdf44*oIa-wld+f@<(#-}x};g$WmIeE;n1;@J<^=PwVBpUKo`{3Ru@^LPf@X!Rx)RTv<mDFWe5svQg7X9&=+_$%mfd~!#q_~X%=Z%<#nes+C+ad`3Fxi53~DkV^fiKRVwes=ic+h->iEBnw-C4I{K&|j|){X6$z%DS@N3ps*DbAl`jx<k<#EQEAl1<^MlKsWy&kt2Y!O9CM86QknquV0<~eo2?a3oKFOPc)IzRzmK6ES<R<Om66?v=?`0V~`TqnrEXBe?DEj>QyU)QJsM*ddo#Q5P#w)mctXraGvF9p9L9k>9K*T7}seqYFBC?>I0BY!6*vSJ-TKNTEu8N4EA{MgNKyUY{;LyPg*MmnvF=?F(I5Y#Ng7Fd~QQL=VncB;$TEXooC@Bg)ymC-aI?M4w=T+bhLFnizZp65TflqmNsZ9g$Q~{Z#Hpj@Y8Q@Kn=s8#%B?|40c^f*p2A*Fd7V}urz~ql;?T(Zo=-S7hF%{wD@w8jJ20k65hr)>LU4U65$S+mKJYzeKRfjfPn`_no`ac+~~DxZ?$UiE!TUa*LxF3J-`k6v2Of<;#=M=x;Kd$L4M=ADs``>g%2lae2Mq}rj7aHqy8T1=jC#<DiER0W{|_<_TYX(Zx?db^=X_&H02J6BvABrYFbi$G6u2#3k~9pYY=aogLvZ_M1r4P!-`k(B^Y(WUTlA4jI-+`o(+Z*EmpG)0P-vtjiPSZ_aR8%aWF0W{2rv@Oq*2p_wFc~ehY)O?ECkD&4pX|<0u}*i8>sk-ipT1mnx&^g#(M*HYt|<A&eV7U`9QPLH%f#od36UW|P2AbKn+%?e1{cY8&`A08uW1fpf_ivO@_vng!r)5@lYF`7vQ`Q<2t=eX0}=@L*?a8zbh)eO)xKQder+NZ4wOg7K7K9}=iA#o!cj<J-3JVFzl|vKj-`MV$}5R@0b?@@`0y-<(x;U-wMMdh-#dy#gIAXz#uzCmDE0)1rYHjT8^~lyx~sdi&)Vjna6&;wo*90-ghL=BVf+=w>+cjAQ9|MBxLT2VL~K0-1hIM^DcworT#H3Fi~i`iWiD_eNDTX@S1fSerL^){-z1OfBg3jmhLB6EO0-J<%m`<OJm0P%ZORM%98t&kr>hJGR??O`FVgWM?q{Cnp`O!KDtY+kh5x@1r)=zvYt))VABnfoJ+CSb%yu3`4$~^LTfc4$zvdHYdibN}hV)ZMGU)t?kEp2o!F}g98nXJ$$cQCaYjG>p%z~6#UttmhQBDdnie>u!;fT4wY(Csjb~&sZCd@CQBa@SerXW=4K)8TC@nxt3BB1p46bte$6u{t^jOXfbBBCO$%^S0h%p-X_DtP+ULG6pi76K(@r=g0uK6P@=;{hL~S`LmYarMiXU)W)f)3scCVHr_UZZ-I!U*gTH7Q6VWye*tqO+WI1=89(uwb+@zI`^<4zQk)g5b)O9J~PK2kG9yx*kvn{r*LQ5A)bC6w+7`^AmadiTBR90f{!ATFX=>k|;>A~M_5qC#>$<%@V>1tKH1<bAIyySG8>As&pk==Ua0p<bJQQ|8~^rf;10)BiT|wmhJpE)YSR?d_bAcXzRGKnEj763I7S9k;4T9$wri?3`NFa%r{c`=+kwQrd1(JRtdnHE&yM&h=?y87wH7W70AUs&0w4`DG2)bV6)nmsO`yoyygGZAc`75*njo+~TIL(>B<HCsAjXg$~*lzG-@K{_U6A<J<(v0&k5K6?5y0)(ZLM{~!CEI}GbDOw3<szw_7KuB^E!DO2#xMZa0tpOh)`=I&#+u=_C4m+U(}{eME2zk@0-OftIqo-68Kpr`*DN;;zzO7Z8Z<e#as3I>fRKH+jjlC{3Ils>oerqr9Qw$yJncMU1^JP8JdB7lT>fF6XKtc^U{L2U$D>r34N>snhC_=T3Kzn%(khXyZO^9#+=30<<hYtAc$W0P8LMg2yzZ|>#VfC16hAk@MlhD&pXSyheHiT3i*w5rJ=6!}Cox^vB7Bu)|djXXrK{b?Lv!h+A&cEa9^Fa}jSQ3rLMXws9G`)4<xS*KODU;9N<e>h2JNr)~wFHXO!eh3#*+_Kyf-aD7@;R?l~Zag<X9%y13cxtcM?mW6SNXVt%L2fPm9`)u+zhiRWJv!{r%Am=doR{{zruF(_F%6Bkh(N;1+3fJ{Fep%@?Q9AYqo*$BUBn2CG_K(m$RxC8v)4|XI3#UxjEpngG#G?@sXq%FQThsx>jP*3Xf)p-m5$$?9De)i==%8V@U2I5!($=w!kFwZZih+Ya*e>4F8Mkn94(UZ66kyt6z9q}!zIwTQmK=l1~RZ1Rd_l)J3D-L{q(!%&!3&uh$dQ75Skz<25}LZdQ@W~X+>65khgwC1x$pySHK-!qXMQ|UV*!YXRn{p0ji^>NL|umM`<Ca{`4n792uMTp|=T&z|Qverj{M0&^UKRIHuo46JtoRUXw1KXpo$8EZn|3Ie+!y<k|7{tCNe81Gqc2p|$e`Z8(4V=IlbB={dA?d=z+96ca^So`88ibP$&ai!TJQ?WTvHmP`u#Y^0aGPpzTXp88q7lB~yxMlCCtQ8d^|QYAA*c6F1r3K<5pu4n@d`^ivsqu4yX)A?DpqXEr)3{9DwKm|eSTJQ{!TafHZPSfc%LYV@aJT!&M6osQ6hH}2FzznO@yb1^j`~y=N{{ZvgA8c;r%2&j=q;gljlMM2sP!Z_!s^!O}Aed_o^+l;9t`(>=*DrSCX7FS-?%>T!V)khg;cC+W9M^O5YihTxw9AXN5iFbt=n|pGLOT~X2gRe|{DiSY(n8#8%C~mlwVRe7?c9p=KE$gE2#osy{JRezu)!V9g*6|aHx2~I&uXI$b#fFWygP?C>G1COPR$ed>gdTG1!iHlU{Pqnf?BXpEm$mVK^-si<t@;kj237`1QIGqt;ZcZ7tJ4K(83~&3nYiAyFls=m_k)`Jne+Hu>0L?Y)e?j%X=aLiyk81DNU)*xeBiPu?G$@wL)y>GiI$7JV1eIYF!RRoHLzl9z%oUTigI(Fm))1_ibY!Q2en*S77miW)FUIo4+0FQ(C^GJ5sx@`P{R-5_62ESEA-}*u$yOgG~^*7xotN30(<$AL&Ui6JnVdrw#e!$tKmj5R1nP>7J*3KuqyR>8U3_Fj5>IP9&hwA;jxg3oNOpk4ItWWw)_64HKkg)SZoj1lA%p`r%a!ntt6RN~d^BBS2CQ!=R@eJ1M$PeFmtf3-UpPA0PEp8_M;R$%m15rVGB4*1|(Z#z5|;(}natRVa*rXj5w_7#CJ(4#kulM5iOdD1UtvzchS*oRgm<Mu9;8P@*N``y=&)p3p0lMr8^_{NqRJAwl7LDrx$HB5huW6a6COR)eiUJK9K@@*2vVQD{LC(@-EOtSX^ujero>yF=BQ{5>``RJ}4VDh3h4Bj=48*0X`Vejr;#Rcv5~^;gJx(~sIKH>!FORlSI+z7DDl94)(5e=N4@kL$GRkHuE~vDhjdRW3J88PrRH+vCL~7)M=}KsQquc-*bVNe=@BfgGb8O@T|1P$m@e@1r70?=4EApiJ+@a=BogrOFT^@oOL1)&y-#qWM<;rpiup-|_3$ahJmCsDhw$k@2hI*Q9SAb+CYNtG^B=GFKrkjVyW(M{$>Rb3k-RW;_=jvcOf=+c_Ghp}Q?Ux)C5R$+>`VISl9AL>>ibdJc4>eLjszUqgVJw@H|vzkYLgp$Mwo^h7-t7>Y2a*s|BJPM)0;h`H#Na3boq@`|10M7r953i0o83efozy_bj1bkYtV@Z`DXNi+3w6<?s!)qDcM9kR9i1AVMna8%WKR9Y+V%%id(an>3vdMA8DCk>^fTLJ6ldiY=z5F7mYTns#373D5az|-olgGM=4&@{w{&qO3$6%Y^o{!BdL00z<U21lOId_&G4dK{*^qL$2zxD{g?%Qft<UMfT26urVzE6LeLz7@*@x#qwk$g!SC?3+@EVTj4X5UXZ7HGnBD@)Bg~yMc-qC(6=fD5KEmclutEQR%^%vuLWvX4U|xCgU?!(Arjcx9D!AJOtGAJ^B87O6L3+{-<k#TthdB)AVSTopv)kNz=T`3m}K{DCPKSA1lUH^t@^#yg*(xjqL+Zc<VT7Mo-CY-Q%*5E=8-PU0TVzyb`{QR#H{ds7l*j-j%IotB|eb@6Vheq9YR1_cV*m1^F~i%hqHKm9ZwPvM1#Fu(~W-d+f4r$RA>LSu_!Swjq4UYJRH2l`QC|coMi|P0zQPOp7N6o@FUs->SZ<y(cDQNs9q$r55r@Z#E9Y-J6};>Q^=UjR{%OY=ENZPRpD91%`g1d5If2q<dYQy*fO3@f!6nOR1?@7IAB^9ae42+WLgU!W88MMU1g+-gx+YVBUupx}Bw!tWf`dp$z~$IS}4)1CWOw5dUm$TQLV=)L-9qGw^xl`z74@dJW!uy>db=RqRdH@XM|6z-<YgL_J5Ys!rnDZ&TN%QXT&nc9{9{?%H0eD{6Q)Lca|&*fi0N8n-~?__omtZ=!B^8qLGe84eAZVQN<P&s$vwX^A+eY{C_%><w6aVA{P!r3+E)Y>}4<)M>^$9j=S%C8<Y<YIDa%g|rgDq~&?{Vba|qta!`16}{HapY$S7VBdT%3PBND8r{enfgGdmw&o4(1qeCf_}S^j%j=70=NFntic<Oc=)2diub&?tJu6C@YzRV2OQT+)0})Dn%Wh4%|1SRfcvE+}A&tidZ$4&E=@$LFxvdwFu+*qGuiu=B$#wno)rI#bPxT~!YpN98I6c(^GjLcFP8VnlHac@1c$bRI1jg}8_&%|CCF7i6XlBIypn!W3+$vWG6HjY39=wpS5>MNW$40=NBn(%k8$lAk7cyRt_OQ823gz*$7wxmdW8fW(?^pB46TiLFv=jGI7VZOQXal{qW|_j;f^Df0F5gH=ats2@JLS_SVLCp=a2(!?B<kgnk@d5JCzjsutFKKrc7DfxL`Pg=r6t*L7E*MgZyYcAa4qOWqbOT6u<SMT$J^7cx(Zo~-~2CG{)CI*PX6z1?i83Om0vQ!Key)1E%r~Pi#q&!+pPIZSM^82U6E>Q+PTMmm4)3tVET8ku<J9yl}&b__!3uS!->f<N$lIXnN}obN&<?9=iKC*a1`mzvDY`UiVwq#5GrPb$FrbUfMH~)eq2w7K^k5U+K3VM#R3Ivjq^rPV&#Xbc9CBEo*vlocfoi}Y1f~|F)TTgYSl51b3Iz0$S^+}@2NN)4Kc(BWGecWktZfB5b&!PnxSx%o9;ng|2OEyx+QKKsT@HVNkz$b*2b_V;U3#;KJtCvNK_6|^ccn~0)@^yIz0A53Xc|IVm6OvP`c-x5^=m2NbWaDH}EdPVB}SQ(`<J7!8Xh=%pmW*KuVt~m(p_}-pG48nuP$l)qmXWKlaVU@r3V^4~1cR(xl(nGLHQbs?AWFwCwNDzmIopD9k~{V0>R{ljKOVfQ&-&6X5Q4E)H5dR|Wm$X8JuXTqxg=d%~V(>A|Gm#O$CbM;K3cHt8Y7FtDynZst*Hdo#>?D^EyOrQA%wo^_lVc073O^qfLeDLDmoo^$Z*ao8OO6H2)9e%1p893%KnJmxI#w^;E)rW#i)#DJKOMskqi(KH&LauJ`|s@dAs^@JiH?O0r-Hia#*ZWqF0&0G4;N=&^C(JZU?<8~>Qb^!|#P+<{h9H$QA$f3d$y#gD?R*jjE*1BEZ?HLx?mAFtwAf`5B5-ST|?JnAOX#}m9f*yGZq+azo?3<q_@L%9#{v7BT%sLE^j$tYSn47c$+%Fg;(_wr|2vfJnDaOhCK*{GE!U;ZvK=i0v$lgL{;lzzfP~OG~zz?pieA<PQ3*88-z5l4Zf2;&|g)q@kaz2<)_HtlTSX+{ix1KaHySEiitAHl?md1{H#=CQvD50@OYZ{3yHn&9PKD?S(O^7dHV*0*sH>RKQDZ0X107&#>c9|lOi#^DLo;j#Lih~A)8+nUy(ELJ200*ArYK~EKXkK(S5rD9TSAGa$x-col1GP!(pySB6<|$k<d&Xndq2$&JIr<su@F4A;XZMQ4ShLBAqscAP7DJR>*<Ojrxc=R0Yt4NTV_TDZW_I*E&pY!KCV_|Xt&pp{N)J!>Yuc{J#Qnf_uV_05Uf@c2h;1yGbY3!ho`#-Vl#q(8j-Tqz=*7?s2gThq56aj?;}!HY;5OB`i$<f}Ll7vI;myP*jluS=HU{4Y17Q5XJDf+bgk21i8MOU*aNo`lUotcaDkmMxYqNTI(4Qz6ad6jo3c5S4(%;uJt}|fi+r{rA{1RaP&|V!D&`C(C-a8N5_Z{Oj>T^iCt(|2OOu={79u@&AhlNhhV75&Q=YLz~^r*LTkw#)?yC#~6>-D2;lik*@xNg;Rr)r!GqAHSC(H^t#Wh>A&bBG$VL4pAp)X4FGIU+_|TvJrxK=r=<5M`zgr><Dsgx*$t8ilYhKaa9HW#qsVsAJqFA?r-Mb{&(UzXv^YgA+cnE*XimCHD;tCQiG0Ku@*P5Es>|twwuW4@n7IZF3Le`+3&SeH-<Q@;wb!yvByc&<vvig<8~>X)QI?I|^~Rt1Ycd6e2)%jcX$+MK1M?SP1LOS<0^o^_{o;#1`A;Rly|{rldt(=SrQc);x<KSG`G#8BogqVhvE#FBL&|pWT(eX#1<w#+B7m9xfWDr4;9Zv}sQKn}?X-P$KHs$~<(2xl*C+Oj02m+@6PuXX=G>)J@4gRZqg8xA4*stphk`U`K(m0iapkA<o^O!Z~U>*KF?l$xP)$?`YvOplpUj8^mtTr#RJRQJmz=2iNgrv@nk4*V+#_$)_^MxOt^%pVHecqQ&bj?ODo7c55uwS=kyCf*Hs*OA>zBoUVDqI;vI0xooLzUo@A|Dp_x}*Bg{Cox85eN@@P3GZh!xEu$*O1YJ48v(e}}okdw#DQ^9;IHSCK7%qi&IXIy<#B<x;%jm`mDv7(IRspK5c5(z%ccEImq5I%@j`9G847XT(?;MR-EyI=NvnMQ?8L+lrfIpTo2HGJC)qEajteRhSY<Qh0Sod06zr;*i&5WBnWp%E@lt1ekr_exltyYD9dyf1f)@uG0_-b7dUveZ5GX99p)h^=mZa4|eyJE`^+Y`;AUh0rnwAC+l(6f&TG~ngu1)ZfXkjCY(X)yW0@F`^5sxai#IJ}7{p`SSl`?JuDIzk#<8IbDWRKNbVZ5WUqZ&P{E49tSHgCea%KUH{)B>dwH*4{I6nW#E^rOU7TYr)@vu?7RqO|ONUr8_UdM0f>SA4Wl%Q8e}%{d~vQD(`7-0zt1w6~2bP0?Q=TN|&SKj>E|ecvUsAiZ0k5UiS+T{y6Lhvr$&Xm=lV=B^alCgw>00Ck2eTrYrlVA8qCxtA>rvEX#!TuZ0$A<4v32q{FC>p5SV(ND4@s+YkDOciM+{mj6T=X5#4WD44=*3BPGT8$?%L$wQiT`#z3u!m_^8?34sB=cbWgRCNL58g<KpS?IkHFz-Hx4qCg!02CDp_#lm|MK=RHZfb4W(mBa*Y}!5yUb1kwVBjY`8@A<eQKyS-4-oGI)t)l=mIl9A10EeH=&D>1wCI(qnyczS3hZtdkdw_^7bo==nLqMO%k*eKZ*VK<2yfdjL|Jmk7L6_0ab?mw2KGYnuww2RVXOsD%j?!_OosL5!fXmNL9}Vj>BD9^quBCtx5JR&ogH=vG1H00CHOZ@!QW~(N%EKY*uYj62t-Mi-^mHl(vB6}qlS^lr$L%VH=zhUP9wRztG&($W^VTb_SRAWbk{62qsD#jEKH-1;hRnxCO2V1K4p~|G@>6(jAKqQWn*!{%PdyS$*M~RXQ!k})INS4&!%B@8Ybwtfy8P|;@hgm(K&VEM$A>|QExPr=T}G>_PF7lFDBh#5>KF~J?~{S7}k$ZUwQ3g?;?(~VI89ldDIE7`qOVl_(Md<|LNDr4`y7XlGH0WSqeu2{D__e!8An=gC)+CrSbmt4y_&X-*V&B9=n`{{6)+0uI+3grFe8i>2LSU=45kcaQxf6bkTd$cG@g)&TQ@M{z5*c-6c+@w=P%G?h;?p;TjI3-4c({Zn?{7x725}JN(7`gOYISJaoRZ57DjRL$vf1T9(kfiPnMd7&YL|ybMr7Y=ixqIx2w-dW|O<Y@7wjg*b6(XV&$)(%H!Stw&C?v}SdOVfVwm{O*_GmPFhD-w|*77-gXPWL`j16TaqrtwKX^my9R%Es#He8rPHjL3G_3ykhJKhl|!SPb-`;Rb<fL{ucREcha(*u$~4zavxeDJ^`}cK~P;}$>P331Tz7ad0fLASv(kw!fNFPn${WNCP8*Wt^AlmCxEq3wh5n6A+3T;sF7gEKhUV2g<Z?L+n~{FG0RJwIdf$FXf!&{79;jP<6_@<mEZKY`j7gZinj;9TU)J1t)5k=qygwVg_pyl3A*WKGUKMmPX^;bN8NbjhF&mY$_j57(my@))UGDClvn+}E<NYx-Gl?U-|}95%Mh*$^?692x7)U#@>`lA-;PZe4m2e(FM5wSnSr+8{uo<gaDEylgrPbV1_dmkV>jhPeEx%>l;6&Ak1g{f$S!T*2ef6~wtNckK(*{Ebz9<kXX0AuxMct9-tEG|anJNH)4c!(Nz}t*&hgj_5_ELqq@EsW<@(A1aOYV#rM?rn@QM~*KKzFM-P59yAoFHP{2_EORx;=W)g53O3^LSev32ILPmD(2+8F&i|A*4}X{?9dx^Kne)+(5Zcx2FJU38yq&^y~!V4;Bum?Um;;L=l<IB-Ps{vwL}X&=jeeL!o~hAcoYVK1o{GPP{VXNSyC9nABs2=u2D!dRR_OVG@MFVKu|5mO?%rg(*Y7O#fl71Ous4q7zGqZW0;XjC<LAFWnf%R5LBjf#cn%ko|>xR>v$gT-3CM7!F;?B%WY%I@Vo!#fiTcyD0bo_KHC<zjRxClVK8WYAVy*x8q{Vrxrh#WW-bs^cIXRxh_|-qw{?t=?nxGVisVt-i_G+<(VMlM?tQfo)ivgjG%O(rpRy)@^xJ^y2kB^f00~ZLga9?E1O(5KV645eBXmi+HN*#(?jLUmJ3#%khplktuFTM<YrQ&5b;YM>bz{Q+Ha_Noiix5+Z6$9&v`<$otys0@~Rmg9lgY@LLt?sN0yQml0-xg$C8(aUmYliEYTbrDU55KAlkUg(_~t=kxm(V;SZX;dWs~nU3UzOKY;HIv`n}tf{X7e9~yt9mN<ZPp6T+u8RS(Kbr;2d7_3=2Qg%C<5976HMbJolSTo-Kr0l<W~1p=9yO16ZBp)t|0vWoPS~nFv2jXo<3F1_8d(1AG3Xa9fdXc=@2c-N{r+})yKUqDO|$vv@s7}q*h{|ROGS0PeiyZ2Q%QFB8hxomlbh~dZ$1L3#~`mby+~_U>-D3@ND`n%d+V_zNm;jd!mVbZ+pXSK*xTi9v&+BLZ4^NP`qF!E4ZZFtN<e2#g;oc9HXrsT$8m;!Bu`;4qycmgpwsqkDMSE=N!O4=B!o}`^`O=oUue)okF^-M*xZPFU1af=QBo84Sm7#3g|CC8TP3Lwqf{V)fJcA0@lzTasn8d1-&~)*^2?`GLFjANSc5|B6hxH1+^$htao5~HPHD9_+2Plm8|^l73SY<EhHt*BmVgGbybg;KjXFr}Yhg|`v96ZZ!hJ!exP-bkOZtL7SM0mIwPc!aF6&CCU0wyA&+cqti?<7P*po_BBB#SeG(sjng>l2+&>k`n#vDCl4*o4~<-d(@aIzSe0n+<wZ>jBGM{!`Ut?&wXReZFLi=yN_x{G_gI@Ui<B5Kk|v^Nl;vL{g{g7kSa)U;&{ltb$fRhKwDy!Aa?r0e2Uo!@D9YtYuP$G2Kuv`~!z(U^KiZ$0Ts*$XjHF8YMRq#;`fE|gyV9lG#p`xCsJ)beK2X_$EZQ84-7VT?Jz1(0~9slAuidO~>!ykHbVzh1vN^oBv|Wx)iUmA#xY)Gf2+q;o*)P?wUQHuO(NZ%zNu*<9CaOy7TVgg98EBBD}}>@s;bDAg$1HIlFo`)Rc8OeJ^WXc_3ydaLbq5o`Kvf<`C$d7cGHMox=z3(VW4$J_gNkfHW;X=AdhRtu)Xj>tr2Y1A#e4gN@6)U1?=*vn0vjefasZm%JKg?>dMn74RHk_RwCQXJRCi-ljPN-wxkDCjP?LTKmXc*uUqa?YQJ1GF=FmvT^WoUXJ}S~Yf0w6R0as<6IQ)Opi+Q|hDKdaaD;M7n579o77}@QccA%Yh9Wqj0qhT;kKhxahKsaemW#{OD10hjoj7zuRg)s_Yv@^|5a^w#|=@(f3UKnl_qEzlf8*wx|o%*L)~-ho@(gELniyel`bDIEu#bZx(ewq(;#)qng>v-u70%Qr;1zK*-k9Of|Fxhbq4m5BGBg9=*4&<p~tG)JsPZU5R9IN*CHn*0^XQ{fN=*ec$#mc#0AVnFfBD8zubog!mg*zx&E$YTp2PM%aygELA6SspJwLg>{DKeBOsW6UQ4|iE3gEiBfS%k1sKPcu;LWm_`qOZ28{C!@4(3qo=KgB1aOBMxHtw?kDlsyTI9iM-30?>)~WD3JcdpQq+9ULiC)h<E(nHYQ@kl0%0>xk(}D<@kHgo;QxK2R?`jZzyq&zTnE@Fx~gQ90+qkMUa?}cQrRT#y4K1K)mx3d)Ro0=qlsmW(*#mophcS;aD<O8i~9~7fm(CP<fX557J>~Efift300h{UefahD0ilGSrbR*PEXQI?Wd}c?La(#1I=w}}CkLL<C%hI-S32?I*9W;k-QaXwR+YI4{4_HqF(Du+yzeftkR{$#CG4UITP8!zoeWlABb1=?Q-tBd#-&UO;zl{#d9+h019aDFuJ}7H5OYmIxr+a*l!MweeY)rRZCyT68oho}afDH{hImE%)HotI*T%@l`&Q?22(;)aOP9k|tF_yHBo_*;Lq(!&u4i+^R@J?2YK>`d#V;G`i=!O(016k%@s|y6+i9s(B%6)sde<3ft@)Ybk1;G0=z&2eQYp?AVS)g0d=n<4U<%S_a9_)bVlM!K-guwp3~2EP^jN$)w|2M$EwQdZr3G#=j}wOxy9&x!$@g+GyA=FhE?6%w`B1CTyt-Ou&77)AN(`DqWorb`%joK|dF6|g3&dpNZR^TkQ%l0REhGLjHQiIYFsXB$epCF1p<et-u}JlE+OpZ$S+gN9Nm`G#ww6|G&*U@YyZU+53t7#1rk#qNg+ULmHys5Do{psm)IMg<AbVeai_)D!ewlpPiRbA3-g>mVZ@+&@hm^3A?O31YbhugPvUSfci9@_wX5}sH!|c<GUELapuKjrA!54UUcdU(=C7D*+M7y2dcGzNxwb|a>-P);?@7>nexzSl9o-qS<<GG6YMLNJ8NF)09CG0dYU<L2BoDlvxw(n{oYETEw=9XyQ*?P3KD~!LpoyR-DZp9p>o4`@33H;d(xKtSS+x<sYDY~khhaU61ON<CL8O(xFwL(5fn2qKv90h;=pa1+nQB3Aa3(=9DmLNbQi=RjHuvcxPl2h@j6<vp8I|{tt<JY-o3BL3zS2btVZ(tUjPs6Z>)t?7{{>NV6y=YS)=Wwb;m1rc>@%5ms+R)-QoSlAKhFL1m|N0-V|Mh=I?DQgw#S2k`Q0D<}7L2aN)3v+5|N0;Q^?xOT7zNP<0h1z!&QhfvKa##P*tF;IXb^bc{`ns#4QyCdpAoo{G^tv>^qbeOU!A{tb3z?^1Hb?LpTDUfm%5gVaWug&J>QO1<2JcV<8j58R)8yuJAq@)Id6_K@ZhA@^=J|`AZEy`0Xa-Y`Zwo8Oet0>JJ5|*b2>+3L>zkGy@K5$(5{|>Ow1K3wPYo{WF@d<X{h0aYt16(Z_1z0+Q9*$tr4}qT&nZ*D}KK~mqD!ZGQqV^q-xkj5A!8!L^UC+=O&8mT$QjSnuOs~p6>4UCcfqwZQ~YHdqh-gYy;hZfzx;tq!=W15~tGun8&uIWaPt$`c)X<cG>6*EZOY2x1!T6*=ey(WVmKH32>*OHCD*Nal^0Wl?%l44kyu=qOrje8&AFJPSbmSdhUH2b(0vD=<#gCUpKtt5Q7GI=iOx1>ELCGU!hUN-9i6VPu-=_l127l`qGYG=m_bX$tX|RMVEL&bfc_REtf!G`Lo00_VKe9zV{zcVIXyt{;C(bLm5T909M?7jA0W5&ZZe_J(^6HxvRnFdK!)Ev}d<sU3W%H9o;&kVoB1$C#3SIf*f5zlqFwOfbj93227e6*(bt*wkYJNpbj6~(LfJias(z;HNjB`{>wjAinpmSzm{Se(`8y4IqPB^-h-h)wg_B!MY)OrkKrAhorhiBKbRA4D}hVrQ(|XP_Z+oQ5OysJ`;uBMe{Vf(*Uu%#I>rUMJDl){SQF!L5CCIx7pnziu%ZLc3gsJmvZKY2uzCByE3o^9cCevW^?<30JkPlI3vsV<Bwyoht$_K!Dp@)!4acF9aK`zOpy`4CZy6ZS#RgckxCeIMGI4}*Ho&yo1w35<x41nbAl2j|QZYN}mq>KyemUcuMXSbC{dHH8R>Px9F|dE5AbmCO7_>2u{BdDbMiX@iTm0X8$5AkV6&e*+x)Snh-tB-H8IPy4Ed0GvmJcUA;xuFF(5_f;c55htu3M);l&I8@`Xn_(iou4e{1Lr9oCKpq8l^^QJ@bbAE%H1H#5}8xK}EO;drZTs`6;L3cdx4JUW641FZud%A0(j`r^iYGwB*hK7StxAjc0#-l1@!Jsyi(Q9Ox0@+sD$IXKIoyzf|5b0<2ixKI`EUSI3>0)*0RD@*!0-Ue6BhPJW$tOEr6w?gdcxs!|%@Amm$%64auX>mU}O5^Z6ba7BP3fB)iV8Qum2bk&MN;|QKYNu``nS^y4T-{q8a){c5Yy?!2LzmISUgiqM_GJ@*iwwB}9X}S_S0T-hmz8^>~WemTI1|X&=AOxZbE&f{FHZAnU`#}SqRu?fsS3n{9Sss7lvOr&pAbJ~g<X5mUN}dJXVbx4D?6wvDvT{%yAK_}BoP~W<0Dt~uZZcRt62#jGs>@QfNVp8f=dWKKKRdfVKYey|?zS9D4|!7bbnwgQ%G3#mF^N^B;6oph#d*lXRQ>7_x*OEF@duT!$OAs?f_Nq?(pQzMugpx?h|Z@Y*=T}S{!KkLB)?$7KpB9)CU1YdP=I@J{e25VBVtTi%U}=Vp7B8(Q0eJ{%!t+^C);P0?15tNG8>O%1MvCVv1Zo)>T7iF_vjYSK?Oh8$MWKjM`WOP^uk4oCukS)#^bLaBAzE-X(s`dilPJ(h;Is=keUTLdzOsqu+dk$asr7alQ4OC@$GBxKq30->t1vt8%V{ncv^V^P0>!Y%x)0WDCmSE(FbfZzi{^9E5oWqA2HJ>L(y64SF(Rrt#;F3J6OL>f<pVed?d`*UwsX`$XR9}nasu&(o+vA6Ut9r@nBP?wH%(P;g};!e;v&EHL{cTp16xX&~BB#h|Jf5wS2W3MRxTW`eC6H4l<*&98-|$BHy`kdOZY!884l$43fl2SI$LAl?46Sehs3?i6*;m+aj^vXE>RNTP>+Ut-jP-sL2UN0K>UfaWU+L^2EYr7%G<*uU}Oh(qKjDe70Xza%Ci!<CkjcT%kxOTJF)mHA$X5`J=}D-Qzzs+4?>Cqb3@(C;rw*R_?LH{AAHSm`+C^`9Rz~>qVL2APsxk?=izBo<!V)6jec6K1q>M^Ib*8oeL+AUN|6qiIGtF)$M$Pt0f22!ndZ=SyC~*7s|l%FueQsipTHiDsf&D?b4JA9g@r{=<peR42d?WYwMJk!f{vX^#rs$TRlQ--`{DSVFEK_FSnTyjL(0R-Asrfs@D=iW({)gEw4jB`SORV=RCs`Pf?HQ{q-F8SV=U9di74+TL^839d|M6p=V#`j{AKWI1FJ6Y6?x;YnVYWovtTi52M<H>U4h@|CJ&nmD~chDzNx&<+gj@4oGa4);6iy^eOV{Cu3ux$gG9T5CmU8Xp-3xIw1XS(u-e!Iyp-${}txKC{>%^LVzVb>c+Cx5IL8$!;~{s!Jh^@p>HhI?7OR$*>NUOIy}Q-hO9Cx)2y~e-|W~)<s>lT+;H{dag>!3(lSfvF<PmT?lA1lM&Zji<sJ7&qx`4+^~aln<7i}9Yjk+_lob4=v!IYBIW<|XEJIl`2*T?i>|;P=G|h+8qftBw%S34zk7$BTrcE+RIR)QpL0c*nJ-P;fBYi#zrs*)ws@#b?jp)i)eCcA+<z1S21|*|rWkXzs-gMrB9?|#^E?@~#+Je7dx}Bqf%l2^zIgM(X2bF-WoVAy`S+ZQoBF1*@hUBWU^6DEmO~Qr!M!uNj5B7p`<J+YKW2&F_h~MM`iZI%s7HRL?ldo+&G{c-wP?Z(NL6N%TgznOeW8|AW6o|-GhNfl?BP62DaJ#(fPtOCoGV|xZ_x^;gMI+c2{)AhJ3v_DWGM*^&6FSIL+Yg4<!2`T=`T(8P#@Cad?wQ)^?}4AtU!(%_I-K-o<Lho5_WNk)P*FefR|!;cjmOBan5vf;$Pr|~xDP8Xzq~5vN?GSJ#zYTV30JTz6u9=omBk=@$*JF9oww*i&}S+tewhM_!t#=YxQ{3KPtZWT6HUG<^wzN>LtDNfFkV%5CqbOHyUBR$S6r!;RqWGXL?g>F2{=vjv|$bxAeuI;@$$7c3!}`+$RxBcsZ*VG@^G&Y^<&$ih)u$Ot*%#)<FK20lZ&0Lm~kzpPqRr{YAHG#jpV+Gn=_@O7q#zlaTudq%3l%Y%MgITV0kh(n7Y+Up*nk)N5RT914@+<k}jFXwAoR9qlJ;G;{j^ZXCqY`5As}iK(XkoL`1n1Rv;RJG+3iW?Yu>@uQ_>&5omZ{!0~BS>dV|Evfc2=)lB64;ylAIaZl)-g7CnTvzNi7XM~6a@HN?!V0E_43v1_@>YdG|>v+3O-QI4~g14J1_EoknOCz#6?qZknGvjmfGk;q#Mmdm!&s7^>+k*_FWm0h^{sVq_8fJJ?6n=50Pa0P`Gd~Uo)<TEi>kTSE*2!w153DS%#bXq2>_Pq4|Lq!C83#!;(e3?Vb!W)zxW-sf+v-yQUpiQfaGCHK-sCF}Lzj$9USq}fFOSkgOt=jKnN=;y$SsHFYtC<j=U4Dqr0dob<lI*l7E3NzRvQou!y6V0TdDzhlb3KDwa>*qm?vo6*}?tC63ZzrP`YU@zpiMo4pur82&867o_WdDPtfev<}83+%~ulPGR_)noF(B)Iwb4VI7=_Fgi;#2DD@Q>Wqf0;ANgXi+3=o8S>c@~F{qEBcaFiAQ|TYChhM@ECvmo>$RKbd2Bkt^lczt<&J9b!jTZF^_AF0u9)06gHpsiWf>Pr~TO9WDy}7EwmO}Ht{M~<Md+;hbiK=qg58-D_$Sb@IVY8}(##}f$|I0snfaUK#7Yi<8N)4#cr#u`W?#PnvjKWt6$8GiM8@;x_{P+K(_nr8H6&laze5}L%!+-6a#NJE?hgav}SSwOsimitC6itDrm_qA&jAuuAi$O5}a`x!LB|6-o!Qi3ya@K)=&%$n)rXF4<g$+(Pk#|Xxc$69*Rxk26ip;iH(?!tHv%ge~fM`L7%9Qh4HX+Mp9U$xSRNcnVUK<0SoEzcbfD9{|fQ1pvSwEF;uUB5LofCsV?|ml1a-sgBWfg04v36;(`k)OZ?^{K=x4!6gBSp_@42z5zN$I}B3p}T-^he>G=HdjixLL*9qIkQsIF-WUgvZ!*pv485;(XS58qX=`nidUj7#FVK;CB5IK3v&XaFXyi8mG$%Kd<97gwi-&>sY4VgF=O~qy8w!?t+O5*jPT?-UY>naB&+fY#hT`=PpP9+{TcQhrrqx5}MjJlH2f3%>eL1N8(X<r@^5D71KvZ4zjO?yTEdt204Y~=U2>o4kpae(&+g->IH<=0><8TIt=>kQdImH&pN2HRs6Df!*zbR^?^ZFH(#*Da%3><KC+4f9lX8f1m?ZvI1=>VP3W-L#=$(X9vT>WAKAr$W~3I2>oKK=!2SW~wcxoGeMElnnUB^*uDxV-Dyu^16Sgo?UUPogcPYW;V!GY%w7U(IE{45``9k6`hL*n$yr-}g7fz~b-GH8e-n(k$LLYtv)t3!XG#8cPg{2eO-p86}OjXw+{;U5Jbb%RrSjh+SFVp;8i~|4d|KTA@f`{KPqC|5?(=BMdC|R?M0IBzo3u?&^=-KMul88u^qqp8){)_*chW&_s|6i42^OEWK)q3|Y0McCb;l=CqE?{UyY1(m}D^7X|$QOTYv;0)L_M2#5cM3rp;q5WZ8F~AG_YU%2K%HOGtxOH4pZjo$`bxm|JoQw#9pVWBStBOfgW5LI#j$<s1#1ooWo@Vj=CJgFHAlrNO*|K@9vFhr*fMYokDfI|&qYBAho_Cw^KsvtLEI$Ap!Ndd{Zc$CEoD#~0Kn+lZ1n=Cu~^5$5}1PRA$`%-QExU{$R?GWAgR{tC~jtHy_-ZCUsA5vJC7aMj*>&Jcfk(1FT)YW{lfj6Zn>IISM5UCueZ*Az4b|)8CRSH0yB5dYL{VO)@%_iOR5#D;u=0Ppd^i!1bKz0@j9pxeqG#V(zf;RV;Kwo8l^DqLw<v-^cc_dpEZv0x@Sw13vjv!cw;&SVAKf;kj4(Jr;BU|wfz(bS9wq((%C5ciCtNu-YA4Mw+}Ce`*=J(>IB^nUK$2tPy^D@!pmY0uj_cfJNMFfgh^FyhiDCvX?5-wk|8*q7jo|@&E3fHPTpPiRdfjreve3EL_QZ6sSosf&vdAHmOmSJCn5=qza$|1)`31yR37t^w}Q=I8N1m;;-y;$fv^q8Li)=U5&iQUQ+o5XS8Lp%5?e+RELIQ$6f>LweviU9Gz65aD}SuSA1dZeFp!fMbJNW(>eak#o)sgIvP4?8rbIpCm^?I&JwsapLnV5QU`wv@Uu?8}E}5&GG6Nk)zwlmucdT1^XJkrTCOZK{%4)Vl8Ve}Q<5dU{rW`|eBm=PEn2}1RhDwYZjhPN{8zd9@%0KqxnCU!l!I2Ql5TnfEZ`V|XUsi_(NUso3dxsV4$F59IG*^nBrmMF_OtSg`1@;xRt&(Fm_Vp!R5FBfezt^lnftS^BPq<-TV16D%)5Q=F!c2{mv6#!ncPIjKGo&HvXE`DeBn=USGYUr6{Wt+k6W<OaapJ_2n0PR0$T~QrHvwN9&=3T3tvp8xa?~2ol_V%!tU!DazOocsVEb{{<Y*y=q7#4cExD2nlUcgbf{ra<$b#aMBPf``f)S38E@1QSa<OX(lOH21bS^6)7Og82<9$^FtY$e0T7L0r?-IY^T&`38&`t=uUp&tGnowzSQEOUJ_YnR07$)&GyCXZ2DlcoxFicPt@8E|2vuYi7D&=>U*1;kiqp$nptfGhKYrs-93c5i5pZmcl2OE|EcM#S=Syi&>FOQOhVY_DIiE(ZAMH2Ol$<e#1htsqk<dd>21dA>wYF-%>Ui)$F5m4}oJ%TkoMGHE`7BH*F99FE@2sfUAqbJ2EG-hW+Q|W3(&_xkhA7Zt>qphRZK`V@t1lzG|j<|fy$A;yy^`5o0GZ=ftE>CO9XUKN)w^(;e=-bPD!opWm%9<3UKx+eRd#}lx=Q?+g8jp))1Y}x9B^i;2+qXtU9%>zG)zl_O03H)}$#&Hx+^u$IZEM+M$Mr$`dQznB$-n&b*nuONjx8)4cB!z~p^fHW{+X704VaT_5sTe~qqqx-IFR%@^)*Q#y8SS<*ekvnYOZ&%N#T=pWN!2$CQ0pBGNI8>650&^TDAPkKk+#yB1>meR7=zANf`Es($=x&xd4#In(z#dq3cvrfP#JyhVoeRb##;9o!y$}uB}YOtTC>)uwlezNdp_;r@IGZiqn0KpRY%8Jf;1_7Sq?_O+o>$UM!M0qDWiQF!}R8q6=!Qy?4l|+X0>2{wIjAkXcZe-Jn4s$m}t0_OEZr&Geeastt0Vnlq5RqEKuvK|%YtYj}eB7?GaT-WG`9+0wFbGklmN!2-6z^p}v41)>j=n{mOkhB0t{z`%)=pl7FfRp@<(!jfqX?N2cnBKvNt{-{r_D{WFwIWR|h-3i&{j+3!2u}Eo_`&Vf?3sVnuB4Z<qZ=bE+|1e-3_N|!_T}PDHY)|5ie*aV3-if<!5#8A}sf@c?F73<Y0sJUDQJ|ywJ7H81Ps@T+VqMFlQ<7}~!88xxe1mwS(*}e5XVOH9q`9eBcbh~^k|>kjl{m$$i#|}y-1AT`>QNSsJ=&!0TfnB?1!9nHiB+R)`IR8K{lCerwXjOTbC?J#2W>n-$i0qlF^h6)-7s0!P!fcM+uWO?O02)F6wDXuGw)IL0{8~$RoEQ+%Sn<;Cg@;DGaT3BFinF&c&%PcGd4EV@&^q}y<qrC#dqEFQw$zVrywtnhS8`8+uED8E?-D5lIKZ0K1app4p#s`im(b|nsIKv)Or)<*BWljl-aV{qv3~NrCLhiX>9UttaMD=XFdfX|IrCBB8tKW{>T>>Xd&JX`cMyMS<J3l1ci?v{mB#TnqHTdfelQU<b|M9{b(>tpcsA0%Ta^Ua8x&}@>J5WT>DlZun3>GvS$Xl!q##JV0AL?Xrd^G{tsFS?eM$2j5vMPikau#j*b~6>ljMbQ5;{Fm(7o+^`h1(wu?eE$|ij{qwNyvP#H-Zf?iG;g4gImMOIQpE0xnkFIqwoDreDyij`5rzNEDxwvj1i#=(b>qeguTG(W#V^$wr-N^w!z*msT%XyXPFpFu0r!@i0hn8FG%)K+<l*pubgvr+En(n3Oi^);pHnYRuqyA^K%f7-2zH*X(QT3hgpe_Iui)$KrKEfX*56mt?l8rv1R+izJ*^6Fidk-Q1hc(kBq&_%}-no?`GFrHCs$J?!81MmvcfpD%-jgdAoyD?i@V?;<5^7;Jg>+}ZG9TV7QyW(+9YyORCE1$;mgGv*2rJHT|zaDYotFOD1_Q~tcnIhc<{M~{5(m~}B^j<Vjq>sYvQJ6eRBvM;Ry&d%m^MeJbhru{Bwmm^ucQe{;tXONvw$+eFk87A>3NuXEEfHzh9OLM0N!t@tRW0Gc%iHx3NXtaGCj#so!<6U35lo#yoGhxSx={Yd4E3E%4=bl$GV26r>6ZhT-%fTw&eAZ+LFH10H8rlI^t)6o9x~~Drt4z>)fKH1T8B#?)8-%*5itWWGHm{+*#*BTdB11OQmZ3qe7ue(d9XZhkXhDFXewy--O;Rv?m-M&c#S3)=LZljU48pt)t?Ist9toCU^HJYL8njt0?PcOg*N|CiaLoqG1?Tbjpmx2B^VbKxD4K!STd9=Pw)420VDa-j$4Or(ISQ*T0bpq6Vu`@-}~`ukk%1WAGrHm)I7rGcZH3gaqc_r;5}Wu2D;?tCTqYrtwh_)?jkU@2Hu^nid)ODS&0Ud>d&8QMKrL#t9d_rVp8rA)x1x>J0)?UJ$TtZizdH7lT1u@t9V!c$?{}(W|5V(ExD>ed$j`vs%>#;9G6K+8IBJ>JtzM6OCw`-G3~&b8)bwwx0PH+9Y4^vk|sjLMh@M*o}2lK%wL{3%P|Zc>S!v;I1hj(gwYR>o^k8IJ3aBBHi+_B>=RGLolMO!P~T`eN>jZyx@EX)g)bT&?L}FeRU0i2?=bC_bsxX!O~mIUnv(He?R?9-yt=q!O{?Xwdav}d+G}e)%*PfPXJuS5!A#k3HtujVtD;V<3tp(?=T9OqSTTN85%D<8g37Y!VFHe}s!xhI-Owp)U!Ii5)Ux<{!m+1_AXe<BhF-nJ7HMZ?u~c`lr{EkM>1SNHfKEJW9G7+w68|kk$WFV)<d@Tv|Kgzx@+(g2zx=2F4Oy1xg*mgy-l!{81w&ph99jOimKf^HvMhIZCQ}j>aY`fjRPSWEF-`zmSF!&5_YM%zL1n6|90R4Z&{4G`$_eN-AB-R;;f-lP3~w4~7Ee!;cp3~iptxZm<5)DX`d`EtE2R1}1zX#bUAyjaV_;VH_B<(UKlyeNufhVVtW)~h%&Ji}Z|zLG?KVTq6lI-j**D_r<T0)dC1u~8-%5|1fLvr4;E0&T@G=az28s2)7h<t24a8+FO?g+>4fCZ5BiopaY~-6qq!Z>+`qUuX6s8T{ZLSj_Ob?ays_!9hb`tjGXU_0a5(r@rR{vpq+r><Am@0Ae*n1vj^$XBGz28TfhbA)erh{G5!itZjH+HoTsu6fC%%r#1w{Z_9jSP`nG;=Qxsk;L07^B1XO!Mx&wfM2bhO39`SQ3*7ns)@Fmjo9v1L&BS#rFA>OF^Mz>%5OVUh1!EcYXrG3xAj~yd@Dm`B~p}cGkQ`eKW12Eo15J;!f%P>CWoA)1C5r)1q#1X<BvCw8fMRjeA&3GE$hRiy^Ed7?LeOeP|FGQR&6OkEGJ_`16XE@`qTWFrRQCJ_y#T++pa+zY~^GKvqYY$YC<jZvjXYcx%)5j7L{v&`_yx=~hb_)N(Rd;|dJ5NYAXn#e7-bd9w$<0Z)8~xwDI=kyP;G(%TS#q0WHDJ#JCdbfCX4UpHb>P*o-(@Acuyi|-C!JUdr0nI)T4=eYE#g0Swue7p7DO!*_p?wU7mbdhkrz80!7@+c<nv(CfhafE@vQSe0FJa)6#h0U_p7>{$+l@Nfd2lL3d%`VIO3QOr3n{aK%T#`q#><|z!w|}H_yTAOy-+4bG655*K(>sr^Yp*VMgdP&!kE$d;zq5RC1cLRtiokWc8m{$K$Kaa?oxCR@{@?1Zueog-iNEJlFuG|+YAjij|HO%#bR64BeN7slrCi#isZ2?<&9fwGD9Vm=<C*&uy?%vzyN7%3!}W_Db^(xB0Hi?0zNDR0mPq_vEP%ygcYlY7?q)u_=T*LdMrZQg%aaq$aT_MC!`$H0omffojJ31~YZLLMaMJYSb57D<f8(V5^&eCbBVz0eBjW<~4<<uH+&WZB-14$A41mixyT|0IB%dppXfLveLen@s?XuG?Ca<Is3o6Rlh?sjc`oXaG9!)#i&CH&nAn}!J;<5j}_kkOYq{c>iTT&~d#w7aifyb%<+oHz0Zs;_&`hiW@ir}=#hOMnh;SP%>EsA-DiE_45sDT~<&q-`Xnbj}`J=X)t%9KLMl%2n7N-6RvsOG;m3G^w06UuOaBGxev2q=E!E|QQY4L_d#m}<dl3L^FA3ZfqaWy15q;pPdBg&u=&zG!)3b0X4wLl<R<gCPl`#m<LwaBk-A*6EQF4qS;pIG5%=7;Z>$`DA1_b3xhmT!t9T(cMM2pUh`h)js>6axgp*DDVI+F}qqu4(5iiCB<MV+bTVj^<z(<fF$x~NjGGosuJ=!>moa_bs<F+SQ2bN_v1K|Y8<RIDp*0i?}LhssQUv=)o*N*>Ba|-YiS}=m=B;$OcqG5$wVt{c|d-uTtLVcis_cof$iO3X$#+@d7{4HsR_lv3{NDqo%>1EaR6x2M(x)tfO^-oOe`e8A@>&>1xG&P<}uJ?76e1KIjCrRGsGU_&ta3;1J0X7msPedK7RbzBZzrS;2Y*d9maBSs{)t&>dgC@6^kXbHfk$uYg^ykYPUC94`AO}Yj19@Z#{U>x=$)eZ;(Vz#NAwPKUjaTdB6Q&L&B#Ki=b&Zp!Pt194jgx_Uo+z=?NXELWD^6T#C@|wzU!$#p<1sIPB1X>RWy(xsqK3uF%W7cWGWd+SnsnUUtFxjkm^)x_J%lra&BSa;WI_jjYTpB$aGWs{v_S4g9zdAjaSU-EJtEPW(a8!z*u+vB@EnTI=lp%`CMRJW(cZHny;eX8O@ms>ly;u7EMx45LU4ZY?U|BNd~y1t5^=sJ7P05YY_a2fn#Z4RdM9U!}xT2nIOXKyn~mt){g|2_PaFK}IaWu(7NX&I#`o4xlDPSx%CCB@IWSWi*0s(9S-7<h3_J+&1HJFxh(+G0CDrZfgyj8_Rk!^Cw}#l5h|5P7;i(X!1r~jbRB@BH~N2nawgLJ@}`=gdOoxx0=<rKmT<3Q@!E6ySI9}!YvKra9mYV{50dQdfNRmuShTYR*~`A4e!-~hk9G@b%+?}U&5}D+$Qo}Kb#C-9Y_tICL5tpK&>Ey3%1doOm4sy($G=MqNzb-G%<}KZDG+Bk2;(7STGDbHKJx#XdR^a31<pbx6BV?ehiTFWcU@`Bs49R5HYAT*RfB7n2A7RkU2$XWJ(ka&6Gz0rld*bhN`BwZHiJGgc6jpYVjoqOTl&P0sIFWV{7})f=d&%ZYcO6enLcYAnC)rolCn=DR-%mUKSL|6=g6%Zc%fc$(^wfA$uvwh7}`z{<WQL<b8PI=(-Vc!F|i0JH5UAr#r8ncYB9BM>{V%TE<)|ntGo{o`x@*D$?a81HFJ9%#&h+8<^XM%1Tx5^~-C#QvKdOSMDis>?_TRmIfoR@V|K?zN*_=$XE+6UkWZh2#=`BTicq4OP+viNfq>Tfs<Gtsoqucp3smxEG%q)2;MVdC^}&F=m4H-T41qra%Hb#$$~0fMf0n*I4$^XmDj~qC;%SLD&#WsJ1m!=m&h_NS;pwna_b4u=)Orbbu$9R3YUn{A(Y!Li?(49Uv^Rn0L5sI<R1Hzxj&MPhgi+&>uqx^<g0W=$Xg5Kl}F)#5VdE45)`E}6vgn7q<hYdj>dUR(%6gGaR+$U>-zl}4aK=Q!Z6&;oMS9buq7x8CeKT=YpTRcP!N>8%ud@10)AGEEfBrm=XQx0_H9<7+PtziMY7+lVeC`gOJwKIdFRh9oj<33S{VV(3oi(>RLBEacded0Rv_wZ8f6~k()yv}UqIL$ZVTt_o`usHWm{}dea4c>c>Yd{O5ZQkp(*9n`+i(85G5A}5K~H^c0m|+(zn>sMAHDo-Mj3iLUHu@4kxo}1>UPS=ro-i8BDc;g=xxREFWxM)c|AoQVB6;imt$&FM_$pWJGp?jftlm<UC<yn0?cz+F-BjYYjU3#N+a#_EB`diGioGe8{7@W#s!t`To#>lv41|rLpZG0e`GkDAG>tg&$59ktsXOXqIP?xh4w9X9{8=R%G@B^khQ{c`O7eE6|&kP-yf^c$u9QDkwMgz^E-#^sT5^QaR1hlJusDOR8Y9AeA((d?*|j)OQOAV25YRx0kur7a6)pNF6I(N^HjoW&Df-#Wl4+5Qh4&HWzQqe-aamXP9}yj;%gmS&Q~*r2_k2tt41xzc#I|LF+)vv~1o3U-%lJ<4W;vYwLos<Em8_@47T4_e>}4&DnkP`Nr6RQ*akg+~0WBV^G;1uXx8o{mZ|m>fhtqCkIMdPEtc3A6Fn1x~JYfO|pnY)=)vGi3vxzjADYQ<4+UXjMGE|{vbJZWjw^pX%+ymn#%jNRFAD8u->i?WTAx~WmyhF^p`nYmT-iQ>T&bG{{}W~ZScQq;`ciIM$_k39a+SiU50pN?r|>n>W?!%M~-Z5tgbaz*EjCgJ{87H2G6n_pYyR?8lJ|TZ}IQ~jD{B=u28?oyxZ<fNqN$Y#o!cA%x-|~hD5B+goUkTpMR7Y1n^yK>cnu0KlWC=<56&ukk$Q@Lj5eq{AX}QRssr0TjyDJeVxxxf{>ri&TeR-SIcFkZhxk{(z*1f-kX;9HCrj)w8;T)#$MI&rtW66%R-^j(vKqQy{7fZq+O{Rle-`*xmrzHuKMcY5h$R4zP{f@UCYLU?|U!slALdUpANH1#hY4gx_%tq)siz$wJ;c8d>&Ul<tC+xFDt|$p--zGA9P+KNagSU1Uaaa%=-v6$$x&!vLNmf1cwITNcOn)=@30Ll*;9pXn8Eqa<YyF?O7o37zQRl`&^kv1AWEh?fm2hfG=iP+se&gfctW(YQyULqrr}r=_GJcsZOpnOLnroS+<j#g|g$K{xqAnJZR02>CfjVF@S7fgo|2WM^XOn*=}VeEg#dnNf8Fi^%lB-2#%ZcAqpbivzB);<EoWsZ4QzLH(VSUF9W-ia+D5B=X5=%!QyG4c!l=Q`Xwy|wOg)s%<5RTYWd4n8z@E6B_G8N8Vf<63>-EQ&1wOUEhj1<UK}xRqxas<o~VU&6-?X$O5V)0&1S3)2Y0I^Rnf&9ChjLAL>kNN7HOfOq<v20&?g)X(suhafr<(y-EDP~#FV?mUYh2wc|E=L@fKF&`g*Jb*_rPNke%F7Hk(^co5>P8zhQ7JOpO;L9)|4b1@_x`>f35G^V1viF|*z-NKPwgw;S!nS%RswS5J+)?`Ke7{(BDfMe<Wa_c~a1*J>ZHmT;7BQpgx~_8h?-y9K=W!ujy%;?{mqaBjR<`rN47&RrB89WxJjxCGR#>@4yx%m9|@Ebx=DKXntRL}D-uArH0<5ZgkJFr`{etv2H7>0B@oo~zE11*%>YZ<uRdzv!BhG??UMrPZKjOK$1^lb79ULuA;Pu>K-O%gl|+a0UJp(`SUvo|UJysCx-&Wwn;?@nsl0+VDZjlb9Qn+|?eH?=9B5L|@Y?)4TvC!WSb9f)cz3MHD;Jow22Q=s|i9rXDy341=*h8Lj{%TL7*KVZxEx&O$h@Hx?~z>gvU{Z;F!aFo?l-lr`1|wOBWrMqX7I;zRGF8a!qz=_K(-UiI7G{{{9q`0xnIAWE}=KXzUCSkl5pPZX8oTgzX5w7N_w$7=O3uH>q}!WjV9{~d~81Z`aTV3%EQHtx5#<uinrK$XSD=C)1ssi-e3x~C+XT57<3@$kU=3W_zVYBkpHFHzMA3~%YmnvLex5|s)4<4w`d)C|AzR=pp+U9?p12t3=}Q8=B#+<D^1nbo%%t-@(Bq2VPK#GJT7yWkHxJVC#71P!r~fbsmO{~1Qka9Ovh?*St=dw^dG+={3(1Y2Xr(}PK3*xfhrU#qFx2ac9@XUHM7rB#nO+K=YGAo21naXd<Hb-)T|{^+C}dvb!=o4Wz+1vk`<W@%I3T<4MHNsT7Dp^5x!H2$UssIt-gqT)6fY)yF)vQq0-cyg;gGld#=lgUzCaYZIepV31UlQfd2AW6KKsUAXwr(-u>li1--O%`V{4K=**r2;8FfWHs%=M8m0MHhElU6e)wJd{{qo{l2lTw)Z5XfX3}Z1W%*vsMJ(rRcEW3=++!ff{;W)kJHZNVP7Oqp8Z9=qKat1x#oQyv`t=_dOot-}@3Iy#eCEvWXQ;6${6Di`$2>eYefO-OIkgyPDA~H1ctzE@5euM)e@Fr^O_10=4mDZBwOr>Wh>3ts{TP?Twg(vbX=NeYCSjhh_&_d=&V@Xr2(jgOB1j38NY~AM=rNb;waD^vWXbQm=fwyy0*DpeRvJ6Ms*&o>ObJ2+3K`xN^V@6{!wYwW>e6msOdLA-JS<U%%`z$@8B0l0DKDf(1kDpfhxI(s>SW*Si?~puQ)fA9yb@`hi#7gAVlknw)eYn`_xd!30hf51S3ap1;tw16E=vweFKxa*$Wy2l#2>1caLi;$d_N_h|j#G@O8f@fqvsJXZ8wIoS&*x913{=rFhIEgq4fS=Q6of?rZ%y;T+8(yD(F&dzXD^3IIoahNDHbT?bsb{nht6iwZEI~I;mrj4gLt}XjHa*>nc5pWnD`20S-tjize8W>my^$pz|a0#8ZQ)m$<qckgfI5UT%7P!6VVP@}56pisxdo*Hw4V0PwfxU6vA4X7C9dZ=z53)%6{vh8jzdv9zut(|guNG=q{<DVj<-gUqUwVB_9i_3XfuN+D7>ao$@rRl8OrO*FKJ_OHLOWtZFqz?0=MaCCc7vQ-u*@27fkkO3GYzwds-z!O@d!~H`+4z9DP7<k|I2^)`TdvQ+>bpxK#bSrA(p@NUIeiAfN?l%b_2HA?SPTXF5;QpQSTCU{IW7}M6|%pUJ~t|Mc@Uf?;{n&$D9R_FF~sPb?5oPUT^=0!<R?hUU%o{*?zZ^54&9^g7o6}(S^~Yrw~|`8sQh*MO~M$BBAC+5^1gsy{(vZi!b4c)lVFb{rJjz84rBH8Hd<o#x#P7c<4LznvBP?dvbG;@3I2zD`fV5dDXFxx)oZIO)ka+y8hT7NX#QP<$7ShWwM25k0+?aV#skwCEgvvIaRA?g`^?u|FB>V(rm7doSrS}zpZQfZ9VnWtSCGM8^70&LpBk-Nd%ZblL>~D_o^Mhh4P^}aOQ>E%37mBLRc6v|Fij;j*IB_+V}*4oAl?iWTcIi5Fy8cDa=yX(u;p#FcRuhBk~GwXG>5n!`Bvryf(m2gVnfwJ1ip_4`ziLzd-yXpD_xn`~Sg6TIH-g+?yE*_J`&&a7yl-M5Cc)>YEPcn3|JuCUX%l>HMpZXQQak_Ui9~t9}F^N}V%S$bcP`A9|gsKLEA^g}~~eKcBJvbT^4d_ujCFAiRs8KYFYDO9xC$@h!yAqA}vlrSv?w5(iN0{v!j2fTAJYUw8-@vDdJ7-y_F=V+0hFuV}z_1%6IM@`TcX+y~zuzUtz9P9Jsme_+zV{tkWG*?+#j+pXxw86LbQ4YgB2(vg8fpK2h$UU1^iM@iK<)4Hj67btm`R%m2A2pwUg$v6Uf9y9=Oi2bN>+Otuk0D<x*$hEVaRA`Nir7BU^)MVHkC3f4*HTBB5sn(`lD>_*kGqE2<Y*C&M!w4cGyJIsz+wbNa7$~C&?>#p6yCUw;Fi6<C1FONo<ZrkF;hU<W6H1fUw3tQd3mI$i6y|2kWBYeSsQ(ayGz+^n6h`sz{2G?NBz+UIjp=pJfA(Aoz*WT*PK{{DpB4r`DzwikiK5}jl^NFVC%9fKVX5hWZQr@B!RObj92M*_`vyke@b@ekj~?IoAK>u_g#')).decode('utf-8')


def get_studio_html(mode: str = "page", initial_context: dict[str, Any] | None = None) -> str:
    """Return the complete 100% offline self-contained Orca Gear Studio HTML5/WebGL2 application.

    Args:
        mode: `"page"` for the wide 3-column OrcaSlicer tab, or `"dock"` for the
            compact right-side docked panel beside OrcaSlicer's 3D Plater.
        initial_context: Optional initial state dictionary (`lang`, `theme`,
            `printer`, `builtin_presets`, `user_presets`, `params`, `export_dir`).
    """
    norm_mode = "dock" if str(mode or "").strip().lower() == "dock" else "page"
    ctx: dict[str, Any] = copy.deepcopy(initial_context) if isinstance(initial_context, dict) else {}

    lang_raw = str(ctx.get("lang") or "pt").strip().lower()
    norm_lang = normalize_language(lang_raw)
    ctx["lang"] = norm_lang

    theme_raw = str(ctx.get("theme") or "dark").strip().lower()
    norm_theme = "light" if theme_raw == "light" else "dark"

    fallback_params = copy.deepcopy(DEFAULT_PARAMS) if isinstance(DEFAULT_PARAMS, dict) else None
    fallback_presets = copy.deepcopy(BUILTIN_PRESETS) if isinstance(BUILTIN_PRESETS, list) else []

    boot_payload: dict[str, Any] = {
        "mode": norm_mode,
        "locales": TRANSLATION_CATALOG,
        "languages": [{"code": c, "name": n} for c, n in zip(SUPPORTED_LANGUAGES, LANGUAGE_NAMES, strict=True)],
        "initial_context": ctx,
        "fallback_params": fallback_params,
        "fallback_presets": fallback_presets,
    }

    html = _STUDIO_UI_HTML_TEMPLATE
    html = html.replace("__INITIAL_LANG__", norm_lang)
    html = html.replace("__INITIAL_THEME__", norm_theme)
    html = html.replace("__INITIAL_MODE__", norm_mode)
    html = html.replace("__ORCA_GEAR_STUDIO_BOOT_JSON__", _studio_ui_safe_json(boot_payload))
    return html

# ===========================================================================
# MODULE: gear_studio.plugin_main
# ===========================================================================

pass  # [bundled] hoisted __future__ import

from collections.abc import Sequence
import copy
import ctypes
import json
import locale
import os
import re
import sys
import threading
import time
import types
from pathlib import Path
from typing import Any, Callable
pass  # [bundled] resolved intra-package import

# Intra-package imports (stripped cleanly when bundled into single-file PEP 723 script)
if "normalize_params" not in globals():
    pass  # [bundled] resolved intra-package import
    pass  # [bundled] resolved intra-package import
    pass  # [bundled] resolved intra-package import
    pass  # [bundled] resolved intra-package import
    pass  # [bundled] resolved intra-package import
    pass  # [bundled] resolved intra-package import
    pass  # [bundled] resolved intra-package import


# ---------------------------------------------------------------------------
# OrcaSlicer `orca` Native Binding Import (with standalone fallback stub)
# ---------------------------------------------------------------------------


def _build_fallback_orca_module() -> types.ModuleType:
    """Create a lightweight stand-in when imported outside OrcaSlicer."""
    mod = types.ModuleType("orca")
    mod._registered_capabilities = []
    mod._requested_permissions = {}
    mod._plugin_cls = None

    class PythonPluginBase:
        def __init__(self) -> None:
            self._stored_config: str = "{}"

        def get_name(self) -> str:
            return ""

        def on_load(self) -> None:
            pass

        def on_unload(self) -> None:
            pass

        def has_config_ui(self) -> bool:
            return False

        def get_config_ui(self) -> str:
            return ""

        def get_default_config(self) -> dict[str, Any]:
            return {}

        def get_config(self) -> str:
            return self._stored_config

        def get_config_version(self) -> str:
            return "1.3.0"

        def save_config(self, config: str) -> bool:
            self._stored_config = str(config or "{}")
            return True

    class BasePlugin:
        def __init__(self) -> None:
            pass

        def register_capabilities(self) -> None:
            pass

    class PagesPluginCapabilityBase(PythonPluginBase):
        def get_ui(self) -> str:
            return ""

        def get_icon(self) -> str:
            return ""

        def on_message(self, data: Any) -> None:
            pass

        def post_message(self, data: Any) -> None:
            pass

    class ScriptPluginCapabilityBase(PythonPluginBase):
        def execute(self) -> Any:
            return None

    class PluginResult:
        Success = 0
        Skipped = 1
        RecoverableError = 2
        FatalError = 3

    class ExecutionResult:
        def __init__(self, status: int = 0, message: str = "", data: str = "") -> None:
            self.status = status
            self.message = message
            self.data = data

        @classmethod
        def success(cls, message: str = "", data: str = "") -> "ExecutionResult":
            return cls(PluginResult.Success, message, data)

        @classmethod
        def skipped(cls, message: str = "") -> "ExecutionResult":
            return cls(PluginResult.Skipped, message, "")

        @classmethod
        def failure(cls, status: int, message: str, data: str = "") -> "ExecutionResult":
            return cls(status, message, data)

    def plugin_decorator(cls: type) -> type:
        mod._plugin_cls = cls
        return cls

    def register_capability(cap_cls: type) -> None:
        mod._registered_capabilities.append(cap_cls)

    def request_permissions(**kwargs: Any) -> None:
        mod._requested_permissions.update(kwargs)

    pages_mod = types.ModuleType("orca.pages")
    pages_mod.PagesPluginCapabilityBase = PagesPluginCapabilityBase

    script_mod = types.ModuleType("orca.script")
    script_mod.ScriptPluginCapabilityBase = ScriptPluginCapabilityBase

    plugin_sub = types.ModuleType("orca.plugin")
    plugin_sub.storage = lambda: str(Path(__file__).resolve().parent)

    class NotificationLevel:
        RegularNotificationLevel = 0
        HintNotificationLevel = 1
        ProgressBarNotificationLevel = 2
        PrintInfoNotificationLevel = 3
        PrintInfoShortNotificationLevel = 4
        ImportantNotificationLevel = 5
        WarningNotificationLevel = 6
        SeriousWarningNotificationLevel = 7
        ErrorNotificationLevel = 8

    host_mod = types.ModuleType("orca.host")
    host_mod.app_language = lambda: "pt_BR"
    host_mod.app_info = lambda: {"version": "2.5.1", "language": "pt_BR"}
    host_mod.preset_bundle = lambda: None
    host_mod.plater = lambda: None
    host_mod.model = lambda: None
    host_mod.selected_printer = lambda: None
    host_mod.plugin = plugin_sub
    host_mod.ui = types.SimpleNamespace(
        NotificationLevel=NotificationLevel,
        create_dock_panel=None,
        create_window=None,
        push_notification=None,
        message=None,
    )
    host_mod.preset = types.SimpleNamespace(
        process=None,
        printer=None,
        filament=None,
    )

    mod.base = BasePlugin
    mod.PythonPluginBase = PythonPluginBase
    mod.PluginResult = PluginResult
    mod.ExecutionResult = ExecutionResult
    mod.plugin = plugin_decorator
    mod.register_capability = register_capability
    mod.request_permissions = request_permissions
    mod.pages = pages_mod
    mod.script = script_mod
    mod.host = host_mod

    return mod


try:
    import orca  # type: ignore[import-not-found]
except ImportError:
    orca = _build_fallback_orca_module()


PLUGIN_SLUG = "orca_gear_generator"
WM_COPYDATA = 0x004A
SMTO_ABORTIFHUNG = 0x0002
ORCA_OTHER_INSTANCE_DWDATA = 1

ICON_SVG_CONTENT: str = """\
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="64" height="64" fill="none">
  <defs>
    <linearGradient id="orcaGearBody" x1="8" y1="20" x2="40" y2="53" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#00E5FF"/>
      <stop offset="48%" stop-color="#00BFA5"/>
      <stop offset="100%" stop-color="#00796B"/>
    </linearGradient>
    <linearGradient id="orcaGearRim" x1="7" y1="18" x2="41" y2="54" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#B2FFFC"/>
      <stop offset="52%" stop-color="#00E5FF"/>
      <stop offset="100%" stop-color="#00897B"/>
    </linearGradient>
    <linearGradient id="orcaPinionFill" x1="33" y1="8" x2="56" y2="31" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFE082"/>
      <stop offset="52%" stop-color="#FFB74D"/>
      <stop offset="100%" stop-color="#F57C00"/>
    </linearGradient>
    <linearGradient id="orcaPinionRim" x1="33" y1="7" x2="57" y2="32" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#FFF8E1"/>
      <stop offset="55%" stop-color="#FFB74D"/>
      <stop offset="100%" stop-color="#E65100"/>
    </linearGradient>
  </defs>

  <!-- Subtle CAD Plater Base Ring (Sibling Identity with Orca Vase Studio) -->
  <ellipse cx="32" cy="56.0" rx="23.5" ry="5.2" stroke="#00BFA5" stroke-width="1.25" stroke-opacity="0.48"/>
  <path d="M12.5 56.0 H51.5 M20.5 52.2 L43.5 59.6 M43.5 52.2 L20.5 59.6" stroke="#00E5FF" stroke-width="0.75" stroke-opacity="0.26" stroke-linecap="round"/>

  <!-- Driven Helical Gear G2 (Orca Emerald-Teal) -->
  <path d="M34.19 29.32 L36.74 29.05 L39.25 28.84 L40.20 31.50 L38.13 32.93 L35.99 34.35 L36.07 36.88 L38.29 38.16 L40.45 39.47 L39.66 42.18 L37.14 42.12 L34.58 42.01 L33.15 44.10 L34.20 46.44 L35.18 48.77 L32.94 50.50 L30.94 48.97 L28.93 47.37 L26.55 48.23 L26.01 50.74 L25.44 53.19 L22.62 53.28 L21.90 50.86 L21.21 48.39 L18.78 47.68 L16.87 49.40 L14.97 51.05 L12.63 49.46 L13.47 47.08 L14.36 44.68 L12.81 42.68 L10.26 42.95 L7.75 43.16 L6.80 40.50 L8.87 39.07 L11.01 37.65 L10.93 35.12 L8.71 33.84 L6.55 32.53 L7.34 29.82 L9.86 29.88 L12.42 29.99 L13.85 27.90 L12.80 25.56 L11.82 23.23 L14.06 21.50 L16.06 23.03 L18.07 24.63 L20.45 23.77 L20.99 21.26 L21.56 18.81 L24.38 18.72 L25.10 21.14 L25.79 23.61 L28.22 24.32 L30.13 22.60 L32.03 20.95 L34.37 22.54 L33.53 24.92 L32.64 27.32 Z" fill="url(#orcaGearBody)" stroke="url(#orcaGearRim)" stroke-width="1.45" stroke-linejoin="round"/>
  <circle cx="23.50" cy="36.00" r="11.30" stroke="#004D40" stroke-width="0.9" stroke-opacity="0.45"/>
  <circle cx="31.73" cy="37.05" r="1.95" fill="#121820" fill-opacity="0.55" stroke="#80FFEA" stroke-width="0.7" stroke-opacity="0.55"/>
  <circle cx="22.45" cy="44.23" r="1.95" fill="#121820" fill-opacity="0.55" stroke="#80FFEA" stroke-width="0.7" stroke-opacity="0.55"/>
  <circle cx="15.27" cy="34.95" r="1.95" fill="#121820" fill-opacity="0.55" stroke="#80FFEA" stroke-width="0.7" stroke-opacity="0.55"/>
  <circle cx="24.55" cy="27.77" r="1.95" fill="#121820" fill-opacity="0.55" stroke="#80FFEA" stroke-width="0.7" stroke-opacity="0.55"/>
  <circle cx="23.50" cy="36.00" r="4.35" fill="#121820" fill-opacity="0.72" stroke="#B2FFFC" stroke-width="1.35"/>

  <!-- Meshed Pinion Gear G1 (Warm Amber-Gold with D-Shaft Bore) -->
  <path d="M40.07 26.32 L38.02 27.32 L35.95 28.18 L34.18 25.90 L35.53 24.11 L37.01 22.38 L36.52 20.05 L34.46 19.08 L32.49 17.99 L33.17 15.19 L35.42 15.13 L37.70 15.21 L39.20 13.37 L38.68 11.15 L38.30 8.94 L40.92 7.72 L42.37 9.44 L43.73 11.27 L46.10 11.30 L47.52 9.51 L49.01 7.84 L51.59 9.13 L51.15 11.33 L50.57 13.53 L52.02 15.41 L54.30 15.40 L56.54 15.52 L57.15 18.34 L55.15 19.37 L53.06 20.29 L52.50 22.60 L53.93 24.37 L55.24 26.20 L53.40 28.43 L51.36 27.51 L49.34 26.45 L47.18 27.45 L46.69 29.68 L46.07 31.83 L43.18 31.79 L42.63 29.62 L42.19 27.38 Z" fill="url(#orcaPinionFill)" stroke="url(#orcaPinionRim)" stroke-width="1.4" stroke-linejoin="round"/>
  <circle cx="44.80" cy="19.50" r="6.80" stroke="#B45309" stroke-width="0.85" stroke-opacity="0.45"/>
  <path d="M41.90 17.80 A3.35 3.35 0 1 0 47.70 17.80 Z" fill="#121820" fill-opacity="0.76" stroke="#FFF3E0" stroke-width="1.25" stroke-linejoin="round"/>

  <!-- Rotation & Pitch Contact Glow Arc -->
  <path d="M11.5 23.0 A18.5 18.5 0 0 1 23.0 13.5" stroke="#00E5FF" stroke-width="1.4" stroke-linecap="round" stroke-dasharray="2.5 2.5" opacity="0.82"/>
  <path d="M21.2 11.8 L24.2 13.4 L21.8 15.8" stroke="#00E5FF" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round" opacity="0.88"/>
  <circle cx="35.75" cy="26.50" r="2.1" fill="#FFF8E1" fill-opacity="0.92"/>
</svg>
"""


# ---------------------------------------------------------------------------
# Cross-Platform Environment, Storage & In-Process Plater IPC (Win32 + macOS)
# ---------------------------------------------------------------------------

_MACOS_PENDING_DISPATCH_CBS: list[Any] = []


def _is_native_orca_host() -> bool:
    """Return True only when running inside the real C++ pybind11 OrcaSlicer host."""
    base_cls = getattr(orca, "base", None)
    return base_cls is not None and type(base_cls).__name__ == "pybind11_type"


def _is_mock_callable(obj: Any) -> bool:
    """Detect unittest.mock objects without importing unittest.mock eagerly."""
    cls_mod = getattr(type(obj), "__module__", "")
    return cls_mod.startswith("unittest.mock")


def _orca_user_config_root(platform_name: str | None = None) -> Path:
    """Return OrcaSlicer's user configuration directory on Windows, macOS, and Linux."""
    plat = platform_name or sys.platform
    if plat == "win32":
        appdata = os.environ.get("APPDATA", "").strip()
        if appdata:
            return Path(appdata) / "OrcaSlicer"
        return Path.home() / "AppData" / "Roaming" / "OrcaSlicer"
    if plat == "darwin":
        return Path.home() / "Library" / "Application Support" / "OrcaSlicer"
    xdg = os.environ.get("XDG_CONFIG_HOME", "").strip()
    base = Path(xdg) if xdg else (Path.home() / ".config")
    return base / "OrcaSlicer"


def _default_installed_plugin_dir() -> Path:
    return _orca_user_config_root() / "orca_plugins" / PLUGIN_SLUG


def _default_plugin_data_dir() -> Path:
    return _orca_user_config_root() / "orca_plugins" / "plugin_data" / PLUGIN_SLUG


def _resolve_storage_dir() -> Path:
    """Resolve current plugin storage folder safely (inside or outside callbacks)."""
    # 1. Try orca.plugin.storage() or orca.host.plugin.storage()
    for holder in (getattr(orca, "plugin", None), getattr(getattr(orca, "host", None), "plugin", None)):
        storage_fn = getattr(holder, "storage", None)
        if callable(storage_fn):
            try:
                raw = storage_fn()
                if isinstance(raw, (str, os.PathLike)) and str(raw).strip():
                    return Path(raw)
            except Exception:
                pass

    # 2. In native OrcaSlicer, prefer `plugin_data/orca_gear_generator`
    if _is_native_orca_host():
        data_dir = _default_plugin_data_dir()
        try:
            data_dir.mkdir(parents=True, exist_ok=True)
            return data_dir
        except Exception:
            pass

    # 3. Fallback to __file__ parent if available
    try:
        here = Path(__file__).resolve().parent
        if here.exists():
            return here
    except Exception:
        pass

    return _default_installed_plugin_dir()


def _format_other_instance_payload(file_paths: Sequence[str | Path]) -> str:
    """Format Win32 `WM_COPYDATA` payload matching `OrcaSlicer.dll` `unescape_strings_cstyle`.

    Produces `"orca-slicer.exe";"<resolved_path_1>";...` where every token escapes
    `\\` -> `\\\\`, `"` -> `\\"`, `\\r` -> `\\r`, `\\n` -> `\\n`, wrapped in double quotes and
    joined by `;` with NO trailing `;` (`OtherInstanceMessageHandler::handle_message` skips `args[0]`).
    """
    resolved_files = [str(Path(p).resolve()) for p in file_paths if str(p).strip()]
    if not resolved_files:
        raise ValueError("file_paths must contain at least one model path")

    tokens = ["orca-slicer.exe", *resolved_files]
    escaped: list[str] = []
    for tok in tokens:
        s = (
            tok.replace("\\", "\\\\")
            .replace('"', '\\"')
            .replace("\r", "\\r")
            .replace("\n", "\\n")
        )
        escaped.append(f'"{s}"')
    return ";".join(escaped)


def _find_orca_mainframe_hwnd(target_pid: int | None = None) -> int | None:
    """Locate OrcaSlicer's `MainFrame` `wxWindowNR` `HWND` in `target_pid` (`os.getpid()` by default).

    Prefers `wxWindowNR` windows marked with OrcaSlicer's `Instance_Hash_Minor` or
    `Instance_Hash_Major` properties, falling back to a visible top-level `wxWindowNR` of that PID.
    """
    if sys.platform != "win32":
        return None

    from ctypes import wintypes

    pid = int(target_pid) if target_pid is not None else os.getpid()
    user32 = ctypes.windll.user32

    WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

    enum_windows = user32.EnumWindows
    if not _is_mock_callable(enum_windows):
        enum_windows.argtypes = [WNDENUMPROC, wintypes.LPARAM]
        enum_windows.restype = wintypes.BOOL

    get_pid = user32.GetWindowThreadProcessId
    if not _is_mock_callable(get_pid):
        get_pid.argtypes = [wintypes.HWND, ctypes.POINTER(wintypes.DWORD)]
        get_pid.restype = wintypes.DWORD

    get_class = user32.GetClassNameW
    if not _is_mock_callable(get_class):
        get_class.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
        get_class.restype = ctypes.c_int

    get_prop = user32.GetPropW
    if not _is_mock_callable(get_prop):
        get_prop.argtypes = [wintypes.HWND, wintypes.LPCWSTR]
        get_prop.restype = wintypes.HANDLE

    is_visible = user32.IsWindowVisible
    if not _is_mock_callable(is_visible):
        is_visible.argtypes = [wintypes.HWND]
        is_visible.restype = wintypes.BOOL

    get_parent = user32.GetParent
    if not _is_mock_callable(get_parent):
        get_parent.argtypes = [wintypes.HWND]
        get_parent.restype = wintypes.HWND

    hash_visible: list[int] = []
    hash_any: list[int] = []
    fallback_visible: list[int] = []

    def _enum_cb(hwnd: int, _lparam: int) -> bool:
        if not hwnd:
            return True
        win_pid = wintypes.DWORD(0)
        get_pid(hwnd, ctypes.byref(win_pid))
        if int(win_pid.value) != pid:
            return True

        cls_buf = ctypes.create_unicode_buffer(64)
        cls_len = get_class(hwnd, cls_buf, 64)
        if cls_len <= 0 or cls_buf.value != "wxWindowNR":
            return True

        minor = get_prop(hwnd, "Instance_Hash_Minor")
        major = get_prop(hwnd, "Instance_Hash_Major")
        vis = bool(is_visible(hwnd))
        hwnd_int = int(hwnd)

        if bool(minor) or bool(major):
            if vis:
                hash_visible.append(hwnd_int)
            else:
                hash_any.append(hwnd_int)
        elif vis and not get_parent(hwnd):
            fallback_visible.append(hwnd_int)
        return True

    cb_ref = WNDENUMPROC(_enum_cb)
    enum_windows(cb_ref, 0)

    if hash_visible:
        return hash_visible[0]
    if hash_any:
        return hash_any[0]
    if fallback_visible:
        return fallback_visible[0]
    return None


class _COPYDATASTRUCT(ctypes.Structure):
    _fields_ = [
        ("dwData", ctypes.c_size_t),
        ("cbData", ctypes.c_uint32),
        ("lpData", ctypes.c_void_p),
    ]


def _dispatch_copydata_to_hwnd(
    hwnd: int,
    payload_str: str,
    timeout_ms: int = 5000,
) -> tuple[bool, str]:
    """Send UTF-16LE `WM_COPYDATA` (`dwData = 1`) to `hwnd` via `SendMessageTimeoutW` (`0x0002`)."""
    if not hwnd or int(hwnd) <= 0:
        return (False, "OrcaSlicer MainFrame HWND not found")
    if not payload_str:
        return (False, "Empty WM_COPYDATA payload")
    if sys.platform != "win32":
        return (False, "WM_COPYDATA requires win32")

    from ctypes import wintypes

    wchar_buf = ctypes.create_unicode_buffer(payload_str)
    cds = _COPYDATASTRUCT(
        dwData=ORCA_OTHER_INSTANCE_DWDATA,
        cbData=ctypes.sizeof(wchar_buf),
        lpData=ctypes.cast(wchar_buf, ctypes.c_void_p),
    )
    result = ctypes.c_size_t(0)

    user32 = ctypes.windll.user32
    send_msg = user32.SendMessageTimeoutW
    if not _is_mock_callable(send_msg):
        send_msg.argtypes = [
            wintypes.HWND,
            wintypes.UINT,
            wintypes.WPARAM,
            ctypes.c_void_p,
            wintypes.UINT,
            wintypes.UINT,
            ctypes.POINTER(ctypes.c_size_t),
        ]
        send_msg.restype = ctypes.c_size_t

    ret = send_msg(
        int(hwnd),
        WM_COPYDATA,
        0,
        ctypes.byref(cds),
        SMTO_ABORTIFHUNG,
        max(100, int(timeout_ms)),
        ctypes.byref(result),
    )
    if not ret:
        err = ctypes.windll.kernel32.GetLastError()
        return (False, f"SendMessageTimeoutW failed (GetLastError={err})")
    return (True, "ok")


class _MacDispatchQueueS(ctypes.Structure):
    pass


def _load_macos_objc_and_gcd() -> tuple[Any, Any]:
    """Load Objective-C runtime (`libobjc`) and GCD (`libSystem`) on macOS (`arm64` & `x86_64`)."""
    for fw in (
        "/System/Library/Frameworks/Foundation.framework/Foundation",
        "/System/Library/Frameworks/AppKit.framework/AppKit",
    ):
        try:
            ctypes.CDLL(fw)
        except OSError:
            pass

    objc = None
    for cand in ("/usr/lib/libobjc.A.dylib", "libobjc.A.dylib", "libobjc.dylib"):
        try:
            objc = ctypes.CDLL(cand)
            break
        except OSError:
            continue
    if objc is None:
        raise RuntimeError("Could not load macOS libobjc.A.dylib")

    libsystem = None
    for cand in ("/usr/lib/libSystem.B.dylib", "libSystem.B.dylib", "libSystem.dylib"):
        try:
            libsystem = ctypes.CDLL(cand)
            break
        except OSError:
            continue
    if libsystem is None:
        raise RuntimeError("Could not load macOS libSystem.B.dylib")

    if not _is_mock_callable(objc.objc_getClass):
        objc.objc_getClass.argtypes = [ctypes.c_char_p]
        objc.objc_getClass.restype = ctypes.c_void_p
    if not _is_mock_callable(objc.sel_registerName):
        objc.sel_registerName.argtypes = [ctypes.c_char_p]
        objc.sel_registerName.restype = ctypes.c_void_p

    return objc, libsystem


def _resolve_macos_app_bundle_path() -> str | None:
    """Find running `.app` bundle path on macOS from `sys.executable` or `/Applications`."""
    try:
        exe_resolved = Path(sys.executable).resolve()
        for parent in exe_resolved.parents:
            if parent.suffix.lower() == ".app" and parent.is_dir():
                return str(parent)
    except Exception:
        pass

    for cand in (
        Path("/Applications/OrcaSlicer.app"),
        Path.home() / "Applications" / "OrcaSlicer.app",
    ):
        try:
            if cand.is_dir():
                return str(cand)
        except Exception:
            continue
    return None


def _dispatch_macos_open_files(
    file_paths: Sequence[str | Path],
    timeout_ms: int = 5000,
) -> tuple[bool, str]:
    """Send model files in-process to OrcaSlicer's Cocoa `wxAppController` on macOS (`darwin`).

    Marshals onto the Cocoa main queue (`_dispatch_main_q`) using ARM64-safe typed `CFUNCTYPE`
    wrappers around `objc_msgSend`, invoking `[NSApp.delegate application:NSApp openFiles:paths]`
    (`GUI_App::MacOpenFiles` -> `Plater::load_files`), with `NSWorkspace` fallback if needed.
    Requires ZERO external `subprocess` permissions.
    """
    if sys.platform != "darwin":
        return (False, "Cocoa openFiles dispatch requires darwin")

    resolved_files = [str(Path(p).resolve()) for p in file_paths if str(p).strip()]
    if not resolved_files:
        return (False, "Empty file_paths for macOS Plater dispatch")

    try:
        objc, libsystem = _load_macos_objc_and_gcd()
    except Exception as exc:
        return (False, f"macOS Objective-C load error: {exc}")

    msg_addr = ctypes.cast(objc.objc_msgSend, ctypes.c_void_p).value
    if not msg_addr:
        return (False, "objc_msgSend address unavailable")

    # Non-variadic ARM64 & x86_64 ABI-safe Objective-C message wrappers
    msg_id0 = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(msg_addr)
    msg_void0 = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p)(msg_addr)
    msg_id_cstr = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p)(msg_addr)
    msg_id_id = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(msg_addr)
    msg_void_id = ctypes.CFUNCTYPE(None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(msg_addr)
    msg_bool_sel = ctypes.CFUNCTYPE(ctypes.c_byte, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(msg_addr)
    msg_bool_id_id = ctypes.CFUNCTYPE(
        ctypes.c_byte, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p
    )(msg_addr)
    msg_void_id_id = ctypes.CFUNCTYPE(
        None, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p
    )(msg_addr)
    msg_open_urls = ctypes.CFUNCTYPE(
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.c_ulong,
        ctypes.c_void_p,
        ctypes.c_void_p,
    )(msg_addr)

    cls_pool = objc.objc_getClass(b"NSAutoreleasePool")
    cls_app = objc.objc_getClass(b"NSApplication")
    cls_str = objc.objc_getClass(b"NSString")
    cls_url = objc.objc_getClass(b"NSURL")
    cls_arr = objc.objc_getClass(b"NSMutableArray")
    cls_ws = objc.objc_getClass(b"NSWorkspace")
    cls_bundle = objc.objc_getClass(b"NSBundle")

    sel_alloc = objc.sel_registerName(b"alloc")
    sel_init = objc.sel_registerName(b"init")
    sel_drain = objc.sel_registerName(b"drain")
    sel_shared_app = objc.sel_registerName(b"sharedApplication")
    sel_delegate = objc.sel_registerName(b"delegate")
    sel_responds = objc.sel_registerName(b"respondsToSelector:")
    sel_open_files = objc.sel_registerName(b"application:openFiles:")
    sel_open_file = objc.sel_registerName(b"application:openFile:")
    sel_str_utf8 = objc.sel_registerName(b"stringWithUTF8String:")
    sel_file_url = objc.sel_registerName(b"fileURLWithPath:")
    sel_array = objc.sel_registerName(b"array")
    sel_add_obj = objc.sel_registerName(b"addObject:")
    sel_shared_ws = objc.sel_registerName(b"sharedWorkspace")
    sel_main_bundle = objc.sel_registerName(b"mainBundle")
    sel_bundle_url = objc.sel_registerName(b"bundleURL")
    sel_open_urls = objc.sel_registerName(
        b"openURLs:withApplicationAtURL:options:configuration:error:"
    )

    done_evt = threading.Event()
    result_box: dict[str, Any] = {"ok": False, "msg": "macOS main-queue callback pending"}

    DISPATCH_FN = ctypes.CFUNCTYPE(None, ctypes.c_void_p)

    def _run_on_cocoa_main(_ctx: int) -> None:
        pool = msg_id0(msg_id0(cls_pool, sel_alloc), sel_init) if cls_pool else None
        try:
            ns_paths = msg_id0(cls_arr, sel_array)
            ns_urls = msg_id0(cls_arr, sel_array)
            for fp in resolved_files:
                ns_s = msg_id_cstr(cls_str, sel_str_utf8, fp.encode("utf-8"))
                if ns_s:
                    msg_void_id(ns_paths, sel_add_obj, ns_s)
                    if cls_url:
                        ns_u = msg_id_id(cls_url, sel_file_url, ns_s)
                        if ns_u:
                            msg_void_id(ns_urls, sel_add_obj, ns_u)

            ns_app = msg_id0(cls_app, sel_shared_app) if cls_app else None
            delegate = msg_id0(ns_app, sel_delegate) if ns_app else None

            if delegate and bool(msg_bool_sel(delegate, sel_responds, sel_open_files)):
                msg_void_id_id(delegate, sel_open_files, ns_app, ns_paths)
                result_box["ok"] = True
                result_box["msg"] = "ok (NSApp.delegate application:openFiles:)"
                return

            if delegate and bool(msg_bool_sel(delegate, sel_responds, sel_open_file)):
                all_ok = True
                for fp in resolved_files:
                    ns_s = msg_id_cstr(cls_str, sel_str_utf8, fp.encode("utf-8"))
                    if not bool(msg_bool_id_id(delegate, sel_open_file, ns_app, ns_s)):
                        all_ok = False
                if all_ok:
                    result_box["ok"] = True
                    result_box["msg"] = "ok (NSApp.delegate application:openFile:)"
                    return

            # Fallback to NSWorkspace openURLs with running bundle URL
            ws = msg_id0(cls_ws, sel_shared_ws) if cls_ws else None
            app_url = None
            if cls_bundle:
                mb = msg_id0(cls_bundle, sel_main_bundle)
                if mb:
                    app_url = msg_id0(mb, sel_bundle_url)
            if not app_url:
                app_path = _resolve_macos_app_bundle_path()
                if app_path and cls_url:
                    ns_app_s = msg_id_cstr(cls_str, sel_str_utf8, app_path.encode("utf-8"))
                    app_url = msg_id_id(cls_url, sel_file_url, ns_app_s)
            if ws and app_url and ns_urls:
                run_app = msg_open_urls(ws, sel_open_urls, ns_urls, app_url, 0, None, None)
                if run_app:
                    result_box["ok"] = True
                    result_box["msg"] = "ok (NSWorkspace openURLs)"
                    return

            result_box["ok"] = False
            result_box["msg"] = "No Cocoa openFiles delegate or NSWorkspace target responded"
        except Exception as inner_exc:
            result_box["ok"] = False
            result_box["msg"] = f"Cocoa main-queue exception: {inner_exc}"
        finally:
            if pool:
                try:
                    msg_void0(pool, sel_drain)
                except Exception:
                    pass
            done_evt.set()

    c_cb = DISPATCH_FN(_run_on_cocoa_main)
    _MACOS_PENDING_DISPATCH_CBS.append(c_cb)

    try:
        main_q = ctypes.cast(
            ctypes.byref(_MacDispatchQueueS.in_dll(libsystem, "_dispatch_main_q")),
            ctypes.c_void_p,
        )
        dispatch_async_f = libsystem.dispatch_async_f
        if not _is_mock_callable(dispatch_async_f):
            dispatch_async_f.argtypes = [ctypes.c_void_p, ctypes.c_void_p, DISPATCH_FN]
            dispatch_async_f.restype = None
        dispatch_async_f(main_q, None, c_cb)
    except Exception as exc:
        if c_cb in _MACOS_PENDING_DISPATCH_CBS:
            _MACOS_PENDING_DISPATCH_CBS.remove(c_cb)
        return (False, f"dispatch_async_f failed: {exc}")

    finished = done_evt.wait(timeout=max(0.2, float(timeout_ms) / 1000.0))
    if finished and c_cb in _MACOS_PENDING_DISPATCH_CBS:
        _MACOS_PENDING_DISPATCH_CBS.remove(c_cb)

    if not finished:
        return (False, "Timed out waiting for Cocoa main-queue openFiles")
    return (bool(result_box["ok"]), str(result_box["msg"]))


def _open_folder_native(folder_path: Path) -> bool:
    """Open `folder_path` in Explorer (Windows) or Finder (macOS) without `subprocess`."""
    resolved = str(Path(folder_path).resolve())
    if sys.platform == "win32":
        startfile_fn = getattr(os, "startfile", None)
        if callable(startfile_fn):
            startfile_fn(resolved)
            return True
        return False

    if sys.platform == "darwin":
        objc, _ = _load_macos_objc_and_gcd()
        msg_addr = ctypes.cast(objc.objc_msgSend, ctypes.c_void_p).value
        if not msg_addr:
            return False
        msg_id0 = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p)(msg_addr)
        msg_id_cstr = ctypes.CFUNCTYPE(
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_char_p
        )(msg_addr)
        msg_id_id = ctypes.CFUNCTYPE(
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p
        )(msg_addr)
        msg_bool_id = ctypes.CFUNCTYPE(
            ctypes.c_byte, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p
        )(msg_addr)

        cls_str = objc.objc_getClass(b"NSString")
        cls_url = objc.objc_getClass(b"NSURL")
        cls_ws = objc.objc_getClass(b"NSWorkspace")
        sel_str_utf8 = objc.sel_registerName(b"stringWithUTF8String:")
        sel_file_url = objc.sel_registerName(b"fileURLWithPath:")
        sel_shared_ws = objc.sel_registerName(b"sharedWorkspace")
        sel_open_url = objc.sel_registerName(b"openURL:")

        ns_s = msg_id_cstr(cls_str, sel_str_utf8, resolved.encode("utf-8"))
        ns_u = msg_id_id(cls_url, sel_file_url, ns_s) if ns_s else None
        ws = msg_id0(cls_ws, sel_shared_ws) if cls_ws else None
        if ws and ns_u:
            return bool(msg_bool_id(ws, sel_open_url, ns_u))
        return False

    return False


def _dispatch_files_to_plater(
    file_paths: Sequence[str | Path],
    timeout_ms: int = 5000,
) -> tuple[bool, str, int | None]:
    """Cross-platform in-process Plater file loader for Windows (`win32`) and macOS (`darwin`)."""
    if sys.platform == "win32":
        copydata_payload = _format_other_instance_payload(file_paths)
        hwnd = _find_orca_mainframe_hwnd()
        ok, msg = _dispatch_copydata_to_hwnd(hwnd or 0, copydata_payload, timeout_ms=timeout_ms)
        return (ok, msg, hwnd)

    if sys.platform == "darwin":
        ok, msg = _dispatch_macos_open_files(file_paths, timeout_ms=timeout_ms)
        return (ok, msg, None)

    return (False, f"Unsupported platform for in-process Plater IPC: {sys.platform}", None)


def _slugify_filename(name: str, fallback: str = "engrenagens") -> str:
    """Slugify filename while scrubbing OrcaSlicer `PluginAuditManager` denied path keywords
    (`secret`, `cert`, `conf` — which C++ `is_denied_path_keyword` blocks case-insensitively).
    """
    cleaned = re.sub(r"[^\w\-. ]+", "", str(name or "").strip(), flags=re.ASCII)
    cleaned = re.sub(r"\s+", "_", cleaned).strip("._-")
    cleaned = re.sub(r"secret", "secr", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"cert", "crt", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"conf", "cfg", cleaned, flags=re.IGNORECASE)
    if not cleaned:
        return fallback
    return cleaned[:64]


def _extract_first_float(val: Any, default: float) -> float:
    if val is None:
        return default
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        f = float(val)
        return f if f == f else default
    if isinstance(val, (list, tuple)):
        for item in val:
            res = _extract_first_float(item, float("nan"))
            if res == res:
                return res
        return default
    s = str(val).strip()
    if not s:
        return default
    m = re.search(r"[-+]?\d*\.?\d+", s)
    if not m:
        return default
    try:
        return float(m.group(0))
    except ValueError:
        return default


def _parse_printable_area(raw: Any, default_x: float = 220.0, default_y: float = 220.0) -> tuple[float, float]:
    """Parse OrcaSlicer `printable_area` into `(bed_x_mm, bed_y_mm)`."""
    if raw is None:
        return (default_x, default_y)

    xs: list[float] = []
    ys: list[float] = []

    tokens: list[Any]
    if isinstance(raw, str):
        s = raw.strip()
        if s.startswith("["):
            try:
                parsed = json.loads(s)
                tokens = parsed if isinstance(parsed, list) else [s]
            except Exception:
                tokens = re.split(r"[;,]+", s)
        else:
            tokens = re.split(r"[;,]+", s)
    elif isinstance(raw, (list, tuple)):
        tokens = list(raw)
    else:
        return (default_x, default_y)

    for tok in tokens:
        if isinstance(tok, (list, tuple)) and len(tok) >= 2:
            try:
                xs.append(float(tok[0]))
                ys.append(float(tok[1]))
            except (TypeError, ValueError):
                continue
        elif isinstance(tok, str):
            m = re.search(r"([-+]?\d*\.?\d+)\s*[xX:]\s*([-+]?\d*\.?\d+)", tok)
            if m:
                try:
                    xs.append(float(m.group(1)))
                    ys.append(float(m.group(2)))
                except ValueError:
                    continue

    if len(xs) >= 2 and len(ys) >= 2:
        dx = max(xs) - min(xs)
        dy = max(ys) - min(ys)
        if dx >= 30.0 and dy >= 30.0:
            return (round(dx, 2), round(dy, 2))

    return (default_x, default_y)


def _parse_line_width(raw: Any, nozzle_mm: float) -> float:
    default_lw = round(nozzle_mm * 1.05, 2)
    if raw is None:
        return default_lw
    if isinstance(raw, (list, tuple)):
        return _parse_line_width(raw[0] if raw else None, nozzle_mm)
    s = str(raw).strip()
    if not s:
        return default_lw
    if s.endswith("%"):
        pct = _extract_first_float(s[:-1], 0.0)
        if pct > 10.0:
            return round(max(0.2, min(2.5, nozzle_mm * (pct / 100.0))), 3)
        return default_lw
    val = _extract_first_float(s, 0.0)
    if val <= 0.05:
        return default_lw
    return round(max(0.2, min(2.5, val)), 3)


def _extract_preset_name(obj: Any, fallback: str = "") -> str:
    if obj is None:
        return fallback
    if isinstance(obj, str):
        return obj.strip() or fallback
    if isinstance(obj, dict):
        for k in ("name", "preset_name", "id"):
            v = obj.get(k)
            if isinstance(v, str) and v.strip():
                return v.strip()
        return fallback
    for attr in ("name", "preset_name"):
        try:
            val = getattr(obj, attr, None)
            if callable(val):
                val = val()
            if isinstance(val, str) and val.strip():
                return val.strip()
        except Exception:
            continue
    return fallback


def _bundle_get_value(bundle: Any, key: str) -> Any:
    if bundle is None:
        return None
    for method_name in ("full_config_value", "config_value", "get"):
        fn = getattr(bundle, method_name, None)
        if callable(fn):
            try:
                val = fn(key)
                if val is not None and val != "":
                    return val
            except Exception:
                continue
    return None


def _detect_language(app_info: dict[str, Any]) -> str:
    raw = app_info.get("language") or app_info.get("lang")
    if raw:
        return normalize_language(raw)
    try:
        return normalize_language(locale.getlocale()[0])
    except Exception:
        return "pt"



def _detect_theme(app_info: dict[str, Any]) -> str:
    theme_raw = str(app_info.get("theme") or app_info.get("color_mode") or "").strip().lower()
    if theme_raw == "light":
        return "light"
    if theme_raw == "dark":
        return "dark"
    if app_info.get("dark_mode") is False:
        return "light"
    return "dark"


def _make_execution_result_success(message: str) -> Any:
    exec_cls = getattr(orca, "ExecutionResult", None)
    if exec_cls is not None:
        success_fn = getattr(exec_cls, "success", None)
        if callable(success_fn):
            try:
                return success_fn(message)
            except TypeError:
                return success_fn(message, "")
        try:
            ok_code = getattr(getattr(orca, "PluginResult", None), "Success", 0)
            return exec_cls(ok_code, message, "")
        except Exception:
            pass
    return {"status": "Success", "message": message}


# ---------------------------------------------------------------------------
# Shared Gear Studio Session & Message Router
# ---------------------------------------------------------------------------


class GearStudioController:
    """Coordinates live OrcaSlicer host reading, gear mesh generation, exports, and Plater IPC."""

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._current_params: dict[str, Any] = normalize_params(DEFAULT_PARAMS)
        self._listeners: dict[str, Callable[[dict[str, Any]], None]] = {}
        self._language_override: str | None = None
        self._language_revision = 0
        self._preferences_loaded = False
        self._last_plater_worker: threading.Thread | None = None
        self._last_plater_outcome: dict[str, Any] = {}

    def _load_ui_preferences(self) -> None:
        """Read callback-scoped SDK storage lazily, never during module import."""
        if self._preferences_loaded:
            return
        try:
            saved = json.loads((_resolve_storage_dir() / "ui_preferences.json").read_text(encoding="utf-8"))
            if isinstance(saved, dict) and saved.get("lang"):
                self._language_override = normalize_language(saved["lang"])
        except (OSError, ValueError, TypeError):
            pass
        self._preferences_loaded = True

    @property
    def current_params(self) -> dict[str, Any]:
        with self._lock:
            return copy.deepcopy(self._current_params)

    def set_current_params(self, raw: dict[str, Any] | None) -> dict[str, Any]:
        norm = normalize_params(raw)
        with self._lock:
            self._current_params = norm
            return copy.deepcopy(norm)

    def get_presets_dir(self) -> Path:
        base = _resolve_storage_dir()
        target = base / "presets"
        try:
            target.mkdir(parents=True, exist_ok=True)
            return target
        except Exception:
            return base

    def get_export_dir(self) -> Path:
        base = _resolve_storage_dir()
        target = base / "exports"
        try:
            target.mkdir(parents=True, exist_ok=True)
            return target
        except Exception:
            fallback = Path.home() / "Documents" / "OrcaGearStudio"
            try:
                fallback.mkdir(parents=True, exist_ok=True)
                return fallback
            except Exception:
                return base

    def read_host_context(self) -> dict[str, Any]:
        """Defensively inspect `orca.host.app_language()` and `orca.host.preset_bundle()`."""
        self._load_ui_preferences()
        app_info: dict[str, Any] = {}
        host = getattr(orca, "host", None)
        if host is not None:
            # Official OrcaSlicer API Reference (`orca.host.app_language()`)
            app_lang_fn = getattr(host, "app_language", None)
            if callable(app_lang_fn):
                try:
                    raw_lang = app_lang_fn()
                    if isinstance(raw_lang, str) and raw_lang.strip():
                        app_info["language"] = raw_lang.strip()
                except Exception:
                    pass

            app_info_fn = getattr(host, "app_info", None)
            if callable(app_info_fn):
                try:
                    info = app_info_fn()
                    if isinstance(info, dict):
                        for k, v in info.items():
                            app_info.setdefault(k, v)
                except Exception:
                    pass

        lang = _detect_language(app_info)
        theme = _detect_theme(app_info)
        theme_explicit = bool(
            app_info.get("theme") or app_info.get("color_mode") or ("dark_mode" in app_info)
        )
        orca_version = str(app_info.get("version") or "2.5.1")

        bundle = None
        if host is not None:
            bundle_fn = getattr(host, "preset_bundle", None)
            if callable(bundle_fn):
                try:
                    bundle = bundle_fn()
                except Exception:
                    bundle = None

        printer_name = "Generic FDM 220x220"
        process_name = "0.20mm Standard"
        filament_name = "Generic PLA"

        if bundle is not None:
            for m in ("current_printer_preset",):
                fn = getattr(bundle, m, None)
                if callable(fn):
                    try:
                        printer_name = _extract_preset_name(fn(), printer_name)
                    except Exception:
                        pass

            for m in ("current_print_preset", "current_process_preset"):
                fn = getattr(bundle, m, None)
                if callable(fn):
                    try:
                        got = _extract_preset_name(fn(), "")
                        if got:
                            process_name = got
                            break
                    except Exception:
                        pass

            for m in ("current_filament_preset_names", "current_filament_presets"):
                fn = getattr(bundle, m, None)
                if callable(fn):
                    try:
                        fils = fn()
                        if isinstance(fils, (list, tuple)) and fils:
                            got = _extract_preset_name(fils[0], "")
                            if got:
                                filament_name = got
                                break
                    except Exception:
                        pass

            if printer_name == "Generic FDM 220x220":
                p_id = _bundle_get_value(bundle, "printer_settings_id")
                if isinstance(p_id, str) and p_id.strip():
                    printer_name = p_id.strip()

        bed_x, bed_y = _parse_printable_area(
            _bundle_get_value(bundle, "printable_area"),
            default_x=220.0,
            default_y=220.0,
        )
        max_z = max(
            50.0,
            min(1000.0, _extract_first_float(_bundle_get_value(bundle, "printable_height"), 250.0)),
        )
        nozzle_mm = max(
            0.15,
            min(2.0, _extract_first_float(_bundle_get_value(bundle, "nozzle_diameter"), 0.4)),
        )
        layer_height_mm = max(
            0.04,
            min(1.2, _extract_first_float(_bundle_get_value(bundle, "layer_height"), 0.2)),
        )
        line_width_mm = _parse_line_width(
            _bundle_get_value(bundle, "outer_wall_line_width"),
            nozzle_mm=nozzle_mm,
        )

        return {
            "lang": self._language_override or lang,
            "lang_explicit": self._language_override is not None,
            "theme": theme,
            "theme_explicit": theme_explicit,
            "orca_version": orca_version,
            "printer_name": printer_name,
            "process_name": process_name,
            "filament_name": filament_name,
            "bed_x": float(bed_x),
            "bed_y": float(bed_y),
            "max_z": float(max_z),
            "nozzle_mm": float(nozzle_mm),
            "layer_height_mm": float(layer_height_mm),
            "line_width_mm": float(line_width_mm),
        }

    def read_full_host_config_snapshot(self, host_ctx: dict[str, Any] | None = None) -> dict[str, Any]:
        """Collect full resolved `project_settings` snapshot from `preset_bundle()` for `.3mf` export."""
        ctx = dict(host_ctx) if host_ctx is not None else self.read_host_context()
        project_settings: dict[str, Any] = {}

        host = getattr(orca, "host", None)
        bundle = None
        if host is not None:
            bundle_fn = getattr(host, "preset_bundle", None)
            if callable(bundle_fn):
                try:
                    bundle = bundle_fn()
                except Exception:
                    bundle = None

        if bundle is not None:
            keys_fn = getattr(bundle, "full_config_keys", None)
            val_fn = getattr(bundle, "full_config_value", None) or getattr(bundle, "config_value", None)
            if callable(keys_fn) and callable(val_fn):
                try:
                    keys = keys_fn()
                    if isinstance(keys, (list, tuple, set)):
                        for k in keys:
                            ks = str(k)
                            if not ks:
                                continue
                            try:
                                v = val_fn(ks)
                                if v is not None:
                                    project_settings[ks] = v
                            except Exception:
                                continue
                except Exception:
                    pass

        ctx["project_settings"] = project_settings
        return ctx

    def build_initial_context(self, mode: str = "page") -> dict[str, Any]:
        host_ctx = self.read_host_context()
        presets_dir = self.get_presets_dir()
        export_dir = self.get_export_dir()
        params = self.current_params
        return {
            "mode": mode,
            "lang": host_ctx["lang"],
            "lang_explicit": host_ctx.get("lang_explicit", False),
            "theme": host_ctx["theme"],
            "theme_explicit": host_ctx.get("theme_explicit", False),
            "printer": {
                "name": host_ctx["printer_name"],
                "process_name": host_ctx["process_name"],
                "filament_name": host_ctx["filament_name"],
                "orca_version": host_ctx["orca_version"],
                "bed_x": host_ctx["bed_x"],
                "bed_y": host_ctx["bed_y"],
                "max_z": host_ctx["max_z"],
                "nozzle_mm": host_ctx["nozzle_mm"],
                "layer_height_mm": host_ctx["layer_height_mm"],
                "line_width_mm": host_ctx["line_width_mm"],
            },
            "builtin_presets": BUILTIN_PRESETS,
            "user_presets": load_user_presets(presets_dir),
            "params": params,
            "export_dir": str(export_dir),
        }

    def _compute_process_preset_updates(
        self,
        params: dict[str, Any],
        host_ctx: dict[str, Any],
    ) -> dict[str, str]:
        """Build mechanical process preset key/value strings for `orca.host.preset.process.begin_update()`."""
        lw = max(0.20, float(host_ctx.get("line_width_mm", 0.42)))
        module_mm = max(0.5, float(params.get("module_mm", 2.0)))
        wall_loops = max(4, min(6, int(round((1.8 * module_mm) / (2.0 * lw)))))

        return {
            "spiral_mode": "0",
            "spiral_mode_smooth": "0",
            "wall_loops": str(wall_loops),
            "top_shell_layers": "5",
            "bottom_shell_layers": "5",
            "sparse_infill_density": "35%",
            "sparse_infill_pattern": "gyroid",
            "elefant_foot_compensation": "0.15",
        }

    def _apply_process_presets(self, updates: dict[str, str]) -> dict[str, Any]:
        """Apply process preset changes on the calling background worker thread.

        NEVER call `orca.host.preset.process.begin_update()` on the wxWidgets UI thread!
        """
        outcome: dict[str, Any] = {"applied": False, "error": None}
        if not updates:
            return outcome
        try:
            host = getattr(orca, "host", None)
            preset_ns = getattr(host, "preset", None) if host is not None else None
            process_ed = getattr(preset_ns, "process", None) if preset_ns is not None else None
            begin_fn = getattr(process_ed, "begin_update", None) if process_ed is not None else None
            if not callable(begin_fn):
                return outcome

            tx = begin_fn()
            if tx is None:
                return outcome

            staged_any = False
            for key, val in updates.items():
                try:
                    tx.set(str(key), str(val))
                    staged_any = True
                except Exception:
                    continue

            if staged_any:
                commit_fn = getattr(tx, "commit", None)
                if callable(commit_fn):
                    commit_fn()
                outcome["applied"] = True
        except Exception as exc:
            outcome["error"] = str(exc)
        return outcome

    def _apply_process_presets_async(
        self,
        updates: dict[str, str],
        delay_sec: float = 0.0,
    ) -> tuple[threading.Thread, dict[str, Any]]:
        """Apply process preset changes strictly on a background daemon thread."""
        outcome: dict[str, Any] = {"applied": False, "error": None}

        def _worker() -> None:
            if delay_sec > 0.0:
                time.sleep(delay_sec)
            res = self._apply_process_presets(updates)
            outcome.update(res)

        thread = threading.Thread(
            target=_worker,
            name="OrcaGearStudio-PresetUpdater",
            daemon=True,
        )
        thread.start()
        return thread, outcome

    def _write_stl_resilient(self, directory: Path, stem: str, mesh: Any, header: str) -> Path:
        target = directory / f"{stem}.stl"
        try:
            return Path(write_binary_stl(target, mesh, header_name=header))
        except PermissionError:
            alt = directory / f"{stem}_{int(time.time() * 1000)}.stl"
            return Path(write_binary_stl(alt, mesh, header_name=header))

    def _notify_host_toast(self, text: str, warning: bool = False) -> None:
        """Show a 3D Plater notification via `orca.host.ui.push_notification(level, text)`."""
        host = getattr(orca, "host", None)
        ui = getattr(host, "ui", None) if host is not None else None
        push_fn = getattr(ui, "push_notification", None) if ui is not None else None
        if not callable(push_fn):
            return

        lvl_enum = getattr(ui, "NotificationLevel", None)
        level_val: Any = None
        if lvl_enum is not None:
            attr_name = "WarningNotificationLevel" if warning else "RegularNotificationLevel"
            level_val = getattr(lvl_enum, attr_name, None)

        try:
            if level_val is not None:
                push_fn(level_val, text)
            else:
                push_fn(0, text)
        except TypeError:
            try:
                push_fn(text)
            except Exception:
                pass
        except Exception:
            pass

    def _run_pair_analysis(
        self,
        params: dict[str, Any],
        host_ctx: dict[str, Any],
        resolution: str = "low",
        prebuilt_meshes: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if prebuilt_meshes is not None and "pinion" in prebuilt_meshes and "gear" in prebuilt_meshes:
            pair_meshes = prebuilt_meshes
        else:
            pinion_mesh = generate_gear_mesh(params, which="pinion", resolution=resolution)
            gear_mesh = generate_gear_mesh(params, which="gear", resolution=resolution)
            pair_meshes = {"pinion": pinion_mesh, "gear": gear_mesh}
        return analyze_gear_pair(params, host_context=host_ctx, meshes=pair_meshes)

    def handle_message(
        self,
        raw_data: Any,
        send_fn: Callable[[dict[str, Any]], None],
        default_mode: str = "page",
    ) -> None:
        """Process incoming WebView2 bridge payload and send responses via `send_fn`."""
        try:
            msg = json.loads(raw_data) if isinstance(raw_data, str) else raw_data
        except Exception as exc:
            send_fn(
                {
                    "type": "action_result",
                    "ok": False,
                    "action": "parse_error",
                    "message": f"Invalid JSON message: {exc}",
                    "paths": [],
                }
            )
            return

        if not isinstance(msg, dict):
            return

        msg_type = str(msg.get("type") or "").strip()
        # Keep at most one sink per actual capability; built-in callables such as
        # list.append are valid too. Reopening replaces the previous view.
        listener_mode = "dock" if default_mode == "dock" else "page"
        self._listeners[listener_mode] = send_fn

        try:
            if msg_type == "ui_preferences":
                self._preferences_loaded = True
                self._language_override = normalize_language(msg.get("lang"))
                prefs = _resolve_storage_dir() / "ui_preferences.json"
                prefs.parent.mkdir(parents=True, exist_ok=True)
                tmp = prefs.with_suffix(".tmp")
                tmp.write_text(json.dumps({"lang": self._language_override}), encoding="utf-8")
                tmp.replace(prefs)
                self._language_revision += 1
                response = {"type": "ui_preferences", "lang": self._language_override,
                            "language_revision": self._language_revision,
                            "language_request_id": msg.get("language_request_id")}
                for mode, listener in list(self._listeners.items()):
                    try:
                        listener(response)
                    except Exception:
                        self._listeners.pop(mode, None)
                return

            if msg_type == "ready":
                mode = str(msg.get("mode") or default_mode)
                init_ctx = self.build_initial_context(mode=mode)
                host_ctx = self.read_host_context()
                params = init_ctx["params"]
                report = self._run_pair_analysis(params, host_ctx, resolution="low")

                send_fn({"type": "init_state", **init_ctx})
                send_fn({"type": "analysis_result", "report": report})
                return

            if msg_type == "analyze":
                params = self.set_current_params(msg.get("params") or self.current_params)
                host_ctx = self.read_host_context()
                report = self._run_pair_analysis(params, host_ctx, resolution="low")
                send_fn({"type": "analysis_result", "report": report})
                return

            if msg_type == "randomize":
                raw_seed = msg.get("seed")
                seed_val: int | None = None
                if raw_seed is not None and raw_seed != "":
                    try:
                        seed_val = int(raw_seed)
                    except (TypeError, ValueError):
                        seed_val = None
                base_params = normalize_params(msg.get("params") or self.current_params)
                randomized = generate_random_printable_params(seed=seed_val, current_params=base_params)
                params = self.set_current_params(randomized)
                send_fn(
                    {
                        "type": "params_updated",
                        "params": params,
                        "source": "randomize",
                    }
                )
                return

            if msg_type == "preset_save":
                params = self.set_current_params(msg.get("params") or self.current_params)
                preset_name = str(msg.get("name") or params.get("name") or "Meu Par").strip() or "Meu Par"
                preset_id = msg.get("id") or msg.get("preset_id")
                preset_id_str = str(preset_id).strip() if preset_id else None
                user_presets = save_user_preset(
                    self.get_presets_dir(),
                    name=preset_name,
                    params=params,
                    preset_id=preset_id_str,
                )
                send_fn(
                    {
                        "type": "presets_updated",
                        "user_presets": user_presets,
                    }
                )
                return

            if msg_type == "preset_delete":
                preset_id = str(msg.get("id") or msg.get("preset_id") or "").strip()
                user_presets = delete_user_preset(self.get_presets_dir(), preset_id=preset_id)
                send_fn(
                    {
                        "type": "presets_updated",
                        "user_presets": user_presets,
                    }
                )
                return

            if msg_type == "export_file":
                incoming_params = copy.deepcopy(msg.get("params") or self.current_params)
                if isinstance(msg.get("export_target"), str) and str(msg.get("export_target")).strip():
                    incoming_params["export_target"] = str(msg.get("export_target")).strip()
                params = self.set_current_params(incoming_params)

                fmt = str(msg.get("format") or "3mf").strip().lower().lstrip(".")
                if fmt not in ("3mf", "stl"):
                    fmt = "3mf"
                export_target = str(msg.get("export_target") or params.get("export_target") or "pair_separated").strip()

                host_ctx = self.read_host_context()
                lang = host_ctx["lang"]
                export_dir = self.get_export_dir()

                target_items = collect_target_meshes(params, target=export_target, lang=lang)
                prebuilt_pair: dict[str, Any] | None = None
                if export_target in ("pair_separated", "full_suite") and len(target_items) >= 2:
                    prebuilt_pair = {"pinion": target_items[0][1], "gear": target_items[1][1]}
                report = self._run_pair_analysis(params, host_ctx, resolution="low", prebuilt_meshes=prebuilt_pair)

                raw_filename = str(msg.get("filename") or "").strip()
                if raw_filename:
                    base_stem = _slugify_filename(Path(raw_filename).stem, fallback="engrenagens")
                else:
                    base_stem = _slugify_filename(params.get("name", "engrenagens"), fallback="engrenagens")

                paths: list[str] = []
                if fmt == "3mf":
                    target_3mf = export_dir / f"{base_stem}.3mf"
                    host_cfg = self.read_full_host_config_snapshot(host_ctx)
                    items_3mf = [(item_name, item_mesh, None) for item_name, item_mesh in target_items]
                    written_3mf = Path(write_orca_3mf(target_3mf, items_3mf, params, host_config=host_cfg))
                    paths.append(str(written_3mf))
                else:
                    if len(target_items) == 1:
                        item_name, item_mesh = target_items[0]
                        stl_path = self._write_stl_resilient(
                            export_dir,
                            base_stem,
                            item_mesh,
                            header=f"OrcaGearStudio:{item_name}",
                        )
                        paths.append(str(stl_path))
                    else:
                        for item_name, item_mesh in target_items:
                            item_slug = _slugify_filename(item_name, fallback="item")
                            stl_path = self._write_stl_resilient(
                                export_dir,
                                f"{base_stem}_{item_slug}",
                                item_mesh,
                                header=f"OrcaGearStudio:{item_name}",
                            )
                            paths.append(str(stl_path))

                ok_msg = (
                    f"Exportado com sucesso ({len(paths)} arquivo(s)): {Path(paths[0]).name}"
                    if lang == "pt"
                    else f"Exported successfully ({len(paths)} file(s)): {Path(paths[0]).name}"
                )
                self._notify_host_toast(translate_message(ok_msg, lang))
                send_fn(
                    {
                        "type": "action_result",
                        "ok": True,
                        "action": "export_file",
                        "format": fmt,
                        "export_target": export_target,
                        "path": paths[0],
                        "paths": paths,
                        "message": translate_message(ok_msg, lang),
                        "report": report,
                    }
                )
                return

            if msg_type == "send_to_plater":
                incoming_params = copy.deepcopy(msg.get("params") or self.current_params)
                if isinstance(msg.get("export_target"), str) and str(msg.get("export_target")).strip():
                    incoming_params["export_target"] = str(msg.get("export_target")).strip()
                params = self.set_current_params(incoming_params)

                export_target = str(msg.get("export_target") or params.get("export_target") or "pair_separated").strip()
                auto_cfg = bool(params.get("auto_configure_slicer", True))

                host_ctx = self.read_host_context()
                lang = host_ctx["lang"]
                export_dir = self.get_export_dir()

                target_items = collect_target_meshes(params, target=export_target, lang=lang)
                prebuilt_pair_plater: dict[str, Any] | None = None
                if export_target in ("pair_separated", "full_suite") and len(target_items) >= 2:
                    prebuilt_pair_plater = {"pinion": target_items[0][1], "gear": target_items[1][1]}
                report = self._run_pair_analysis(
                    params, host_ctx, resolution="low", prebuilt_meshes=prebuilt_pair_plater
                )

                base_stem = _slugify_filename(params.get("name", "engrenagens"), fallback="engrenagens")
                stl_paths: list[str] = []
                for item_name, item_mesh in target_items:
                    item_slug = _slugify_filename(item_name, fallback="peca")
                    stl_file = self._write_stl_resilient(
                        export_dir,
                        f"{base_stem}_{item_slug}_plater",
                        item_mesh,
                        header=f"OrcaGearStudio:{item_name}",
                    )
                    stl_paths.append(str(stl_file))

                updates: dict[str, str] = {}
                if auto_cfg:
                    updates = self._compute_process_preset_updates(params=params, host_ctx=host_ctx)

                native_host = _is_native_orca_host()
                ipc_delay = 0.06 if native_host else 0.01
                preset_delay = 0.45 if native_host else 0.01
                dispatch_outcome: dict[str, Any] = {
                    "ipc_ok": False,
                    "ipc_message": "",
                    "hwnd": None,
                    "platform": sys.platform,
                    "thread_id": None,
                    "preset_applied": False,
                    "preset_error": None,
                }
                self._last_plater_outcome = dispatch_outcome

                def _plater_bg_worker() -> None:
                    dispatch_outcome["thread_id"] = threading.get_ident()
                    if ipc_delay > 0.0:
                        time.sleep(ipc_delay)

                    ipc_ok, ipc_msg, hwnd = _dispatch_files_to_plater(stl_paths)
                    dispatch_outcome["hwnd"] = hwnd
                    dispatch_outcome["ipc_ok"] = ipc_ok
                    dispatch_outcome["ipc_message"] = ipc_msg

                    if auto_cfg and updates:
                        if preset_delay > 0.0:
                            time.sleep(preset_delay)
                        preset_res = self._apply_process_presets(updates)
                        dispatch_outcome["preset_applied"] = bool(preset_res.get("applied", False))
                        dispatch_outcome["preset_error"] = preset_res.get("error")

                worker = threading.Thread(
                    target=_plater_bg_worker,
                    name="OrcaGearStudio-PlaterDispatch",
                    daemon=True,
                )
                self._last_plater_worker = worker
                worker.start()

                if not native_host:
                    # Safe to join in standalone/test harness; NEVER join on native wxWidgets UI thread!
                    worker.join(timeout=6.0)
                    slicer_configured = bool(dispatch_outcome.get("preset_applied", False))
                else:
                    process_ed = getattr(
                        getattr(getattr(orca, "host", None), "preset", None),
                        "process",
                        None,
                    )
                    slicer_configured = bool(auto_cfg and hasattr(process_ed, "begin_update"))

                msg_text = (
                    f"Enviado para a mesa do OrcaSlicer ({len(stl_paths)} peça(s))."
                    if lang == "pt"
                    else f"Sent to OrcaSlicer Plater ({len(stl_paths)} part(s))."
                )
                self._notify_host_toast(translate_message(msg_text, lang))

                send_fn(
                    {
                        "type": "action_result",
                        "ok": True,
                        "action": "send_to_plater",
                        "export_target": export_target,
                        "path": stl_paths[0],
                        "paths": stl_paths,
                        "message": translate_message(msg_text, lang),
                        "report": report,
                        "slicer_configured": slicer_configured,
                    }
                )
                return

            if msg_type == "open_exports_folder":
                export_dir = self.get_export_dir()
                lang = self.read_host_context()["lang"]
                startfile_fn = getattr(os, "startfile", None)
                if _is_native_orca_host() or _is_mock_callable(startfile_fn) or _is_mock_callable(_open_folder_native):
                    try:
                        _open_folder_native(export_dir)
                    except Exception:
                        pass

                msg_text = (
                    f"Pasta de exportação: {export_dir}"
                    if lang == "pt"
                    else f"Exports folder: {export_dir}"
                )
                send_fn(
                    {
                        "type": "action_result",
                        "ok": True,
                        "action": "open_exports_folder",
                        "path": str(export_dir),
                        "paths": [str(export_dir)],
                        "message": translate_message(msg_text, lang),
                    }
                )
                return

            send_fn(
                {
                    "type": "action_result",
                    "ok": False,
                    "action": msg_type or "unknown",
                    "message": f"Unsupported message type: {msg_type!r}",
                    "paths": [],
                }
            )
        except Exception as exc:
            send_fn(
                {
                    "type": "action_result",
                    "ok": False,
                    "action": msg_type or "error",
                    "message": str(exc),
                    "paths": [],
                }
            )


_SHARED_CONTROLLER = GearStudioController()


# ---------------------------------------------------------------------------
# OrcaSlicer Plugin Capabilities (Top-Bar Page + Docked Side Panel)
# ---------------------------------------------------------------------------


class GearStudioPageCapability(orca.pages.PagesPluginCapabilityBase):
    """Full-screen top-bar tab (`Gerador de Engrenagens`) beside Prepare / Preview / Device."""

    def __init__(self, controller: GearStudioController | None = None) -> None:
        super().__init__()
        self._controller = controller or _SHARED_CONTROLLER

    def get_name(self) -> str:
        return "Gerador de Engrenagens"

    def get_default_config(self) -> dict[str, Any]:
        return {
            "default_gear_type": "spur",
            "default_module_mm": 2.0,
            "default_export_target": "pair_separated",
            "auto_configure_slicer": True,
        }

    def get_icon(self) -> str:
        storage_dir = _resolve_storage_dir()
        existing_candidates: list[Path] = []
        try:
            existing_candidates.append(Path(__file__).resolve().parent / "icon.svg")
        except Exception:
            pass
        existing_candidates.extend(
            [
                storage_dir / "icon.svg",
                _default_installed_plugin_dir() / "icon.svg",
            ]
        )
        for cand in existing_candidates:
            try:
                if cand.is_file() and cand.stat().st_size > 0:
                    return str(cand)
            except Exception:
                continue

        # Auto-materialize embedded `icon.svg` when user side-loaded only `orca_gear_generator.py`
        write_targets: list[Path] = [
            storage_dir / "icon.svg",
            _default_plugin_data_dir() / "icon.svg",
        ]
        try:
            write_targets.append(Path(__file__).resolve().parent / "icon.svg")
        except Exception:
            pass
        write_targets.append(Path.home() / "Documents" / "OrcaGearStudio" / "icon.svg")

        seen_dirs: set[str] = set()
        for target in write_targets:
            key = str(target)
            if key in seen_dirs:
                continue
            seen_dirs.add(key)
            try:
                target.parent.mkdir(parents=True, exist_ok=True)
                with open(target, "w", encoding="utf-8", newline="\n") as fh:
                    fh.write(ICON_SVG_CONTENT)
                if target.is_file() and target.stat().st_size > 0:
                    return str(target)
            except Exception:
                continue
        return ""

    def get_ui(self) -> str:
        initial_ctx = self._controller.build_initial_context(mode="page")
        return get_studio_html(mode="page", initial_context=initial_ctx)

    def post_message(self, data: Any) -> None:
        super_post = getattr(super(), "post_message", None)
        if callable(super_post):
            super_post(data)

    def on_message(self, data: Any) -> None:
        self._controller.handle_message(
            raw_data=data,
            send_fn=self.post_message,
            default_mode="page",
        )


class GearStudioDockCapability(orca.script.ScriptPluginCapabilityBase):
    """Opens/shows a docked right-hand Gear Studio panel directly beside the 3D Plater."""

    _active_panel: Any = None
    _panel_lock = threading.RLock()

    def __init__(self, controller: GearStudioController | None = None) -> None:
        super().__init__()
        self._controller = controller or _SHARED_CONTROLLER

    def get_name(self) -> str:
        return "Orca Gear Studio - Painel Lateral"

    def get_default_config(self) -> dict[str, Any]:
        return {
            "default_export_target": "pair_separated",
            "auto_configure_slicer": True,
            "dock_side": "right",
        }

    def get_ui(self) -> str:
        initial_ctx = self._controller.build_initial_context(mode="dock")
        return get_studio_html(mode="dock", initial_context=initial_ctx)

    def _post_to_panel(self, payload: dict[str, Any]) -> None:
        with self._panel_lock:
            panel = GearStudioDockCapability._active_panel
        if panel is None:
            return
        try:
            is_open_fn = getattr(panel, "is_open", None)
            if callable(is_open_fn) and not is_open_fn():
                return
            post_fn = getattr(panel, "post", None)
            if callable(post_fn):
                post_fn(payload)
        except Exception:
            pass

    def _on_panel_message(self, data: Any) -> None:
        self._controller.handle_message(
            raw_data=data,
            send_fn=self._post_to_panel,
            default_mode="dock",
        )

    def _on_panel_close(self) -> None:
        self._controller._listeners.pop("dock", None)
        with self._panel_lock:
            GearStudioDockCapability._active_panel = None

    def on_message(self, data: Any) -> None:
        """Direct message entry point for testing or programmatic invocation."""
        self._on_panel_message(data)

    def execute(self) -> Any:
        """Invoked on OrcaSlicer's background Script worker thread."""
        with self._panel_lock:
            existing = GearStudioDockCapability._active_panel

        if existing is not None:
            try:
                is_open_fn = getattr(existing, "is_open", None)
                if not callable(is_open_fn) or is_open_fn():
                    show_fn = getattr(existing, "show", None)
                    if callable(show_fn):
                        show_fn()
                    init_ctx = self._controller.build_initial_context(mode="dock")
                    self._post_to_panel({"type": "init_state", **init_ctx})
                    return _make_execution_result_success("Painel lateral Orca Gear Studio exibido.")
            except Exception:
                with self._panel_lock:
                    GearStudioDockCapability._active_panel = None

        html = self.get_ui()
        host = getattr(orca, "host", None)
        ui = getattr(host, "ui", None) if host is not None else None
        create_dock_fn = getattr(ui, "create_dock_panel", None) if ui is not None else None

        if callable(create_dock_fn):
            panel = create_dock_fn(
                html,
                title="Orca Gear Studio",
                width=430,
                height=800,
                on_message=self._on_panel_message,
                on_close=self._on_panel_close,
                dock="right",
            )
            with self._panel_lock:
                GearStudioDockCapability._active_panel = panel
            if panel is not None:
                show_fn = getattr(panel, "show", None)
                if callable(show_fn):
                    try:
                        show_fn()
                    except Exception:
                        pass
            return _make_execution_result_success("Painel lateral Orca Gear Studio aberto.")

        create_win_fn = getattr(ui, "create_window", None) if ui is not None else None
        if callable(create_win_fn):
            panel = create_win_fn(
                html,
                title="Orca Gear Studio",
                width=450,
                height=820,
                on_message=self._on_panel_message,
                on_close=self._on_panel_close,
            )
            with self._panel_lock:
                GearStudioDockCapability._active_panel = panel
            return _make_execution_result_success("Janela Orca Gear Studio aberta.")

        return _make_execution_result_success("Orca Gear Studio pronto.")


# ---------------------------------------------------------------------------
# Single `@orca.plugin` Entry Point Class
# ---------------------------------------------------------------------------


@orca.plugin
class OrcaGearStudioPlugin(orca.base):
    """OrcaSlicer 2.5.1+ Native Plugin Entry Point for Orca Gear Studio."""

    def __init__(self) -> None:
        super().__init__()

    def register_capabilities(self) -> None:
        """Declare required plugin permissions and register Page + Script Dock capabilities.

        Per OrcaSlicer's `Plugin Audit Hook` specification:
        - `data_dir()` (`orca_plugins` and `orca.host.plugin.storage()`) is already a global
          read+write Allowed Root requiring zero `fs_read`/`fs_readwrite` prompts.
        - `has_permission` uses exact string equality (glob wildcards like `/*` are invalid).
        - `threading=True` declares the fixed `"thread"` audit target once up front.
        """
        req_fn = getattr(orca, "request_permissions", None)
        if callable(req_fn):
            req_fn(threading=True)

        orca.register_capability(GearStudioPageCapability)
        orca.register_capability(GearStudioDockCapability)
