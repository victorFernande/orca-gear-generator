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
_STUDIO_UI_HTML_TEMPLATE = _gear_ui_zlib.decompress(_gear_ui_b64.b85decode(b'c-ri}YmXzzks$b8zrve?X^@pkCK=4k%F3!rEh`^YDdlUD>@IcJ7Pvt&n2ait!Hx*#qgu6)`W7>|#m?U0B#dSU2h3^q7FrD;tY#W}GnfPBgYvuXKlCq{pKxa8k8t;h;3KQ5rNyeHN|OFCH#avoH#avofArDb>2B+@vwb#*N5h@(Ji-q)bjKHu3+?vd$zkiTanwF)oIGu}3#{kHZaE%!BTvt5J=;Ithit6vxjpz8d9lm712>Gk_;Fzx_sd%awk9*iF4n*Fy{kzO#s$_5#<4esf>(Yo9z5=OmwwkP(~ni=kNwzphvlg24!y^<N|ghO{dnl@oQ7SOJ@wp>HREZ|4<4=Y^zS^1;v4+j4uc?G{mu&=@tzyLF1%!4euuGgxpPr=CzEaVN41UG{aWXtOq{r5Z-~h~r|N8~<gOd`Ak|rSw(3<QwLAzey%6&{^=jQ!dH#4ZjS<jhZL8K($+Gw5IKb8&$GKmxrE@z0)veX)wJnu9m;w&rMaL~V^;PC<uCh9ORx4XuB~c~_dtO+MrX3&#)UVg-o9i_*FAjt81>~*Q*E<^m-PpU1%OlqxL%Qeno&J42eHwe%_Xn=K-dWc&dj1HKH+%Q*ZwVX&7?!fz?ZTi!PPOW8J=jd;D1ue1oxZz~&X0nAEc#hpWwi%2__Miz9j$GY(#3hlvMa1h%3J`iI0<U&{RiFt13gP?^!@{=zX8;B)*l$HMzI@DqjK<?kne77)Q$8jH$(#V`@jfQBc~hsG39JH8;-~sxV_*?G+Sj`lWS-W{>Wa4|5xgpqVdq}`2Z>cnr}|7jkFOA&jTxM2xDAxWMV%+y1L_Nn_aqLQ4kPQS6QLyT?8Kc<gl>Ha83-pa&!~L-e{FQ8T#Yb$8NVtzYnPRc>uf_tg=r!({VgqWeBw#d7<AgX>E;yaj?w_yDm)Mp6{~VpyvVn-C!IALpQ=!500Ts`P{ph4&4y)uu3#>yWYd^y#0<jbBF%LAWlzRuh*~jH&au$Pyg9dx4+T9-|u8kUC;IU8X!4!EkM@P?RCAn*Ug){-OXOL*Ug%`8^D>#pK9enEob)j)}e`w?AhDd>^j|kdiK^jAW^y*vllqe+w7-i@BIf`8yRzy7<}u&{m!h}d;h^^XYTB+--kaAiK&{i$n4cBtZ!t`UT0&o?salzFV=qm^VX?v7>(+ax3>A9yS|w<d3)>k``MGX_n=;NHWrw?H5%Ggwodc6RxJ@f-y`Pj1lQ%rf8*mAiXnw01UhoV3mided*b$bRHjOGacN$K^1T}ZLJK6!?rQaqvGBmd*^&Il@#znPt8F&$dp&QAX&txw`XUUb<DL`%d=e3Dy1_6AWx8S}%A&d4cSrv4Mix+_Bq;zr@=)4TguDT%;guCyl{&2s(+K(38+u(x90y~MNO|RTUi+~CI)XKOK>c>dxc2*Q<n@RG+uO2a)D45-umdZ<MhYPiWs~&tZC0gn90DcyP-rB9)G>&j5ZEiX;$S-Jq$&zp>XVbmB2u_42I2f*21W>Yn`TuGcx}3HUg}KaI2faf1ab-_FcFn18{_4V2OySXYnZfDG4Lt{KvyEtr+~w~;gCS~{Ae<C0bGCR5tZ>1q(=yC`T=k(K$(t+%Vshr0AIVuo`IeS9eo1hcW+I#HsGn5%>f%+jLSZ(KR`&Nffr)(t7#Pb{hPATA-5SV9p#P}UwNG8FWd>X%~?auDBumXE@sXOT1E6h1bH3@AS-K76BaMOXN@|E>yn~OGzekQ6chOktR+3~dYd_XCRaMZX}vNwI$5f_)ETkHkNk02klKJc3@!qFRyfwQkiRYFyq_ipPGDfo3oHUC6l?X3o_Db-RW?@r<5jr;(CAX{?>urzmS9M2;Z2j2L@3E$6umH#B!07$zq$~;f;_nUD2Kt-@^rt?XRicATa9G8T?z8u=j(<p5$lx=ArZYeMqU9P<#Jt$%Bul1N$DO+#jDVr@TPEG<0#WC&yzetS<(1)5k|E*fEQB=X33Z^bxz@wu-B3#1vWVaW~?VtLfjX0A;If&IU<mv+N5<yNC}$|+x?(Bjffn<G)6{ERudgUuJEi(fSGVGCcZ7<{4uRui?GC|C03A14>G6Mg9kH&4QioFj$H<IQN>HG#<dv?hU&((lp*zXAtSRC2WlY6fJMQdM1EvavKPd<+_`Uxo%@+&+2Cu$%+-$Tnwg>%o9C+rltuoDmY>#w2eUwT;_+QrV}@wcTU1=Lk;^q%Q*w#<J(Jhw>3i06HkeAvt?o385XdC(We<(HtPsGNydJHlW;do$jeZc0AfdVy&5(yUAY4b<9tUx88^*=$41w$O<zlkIE9J=sTW=HXAVXbxSq&+Kg~~W|WAC#fj7L&gR^So}<$ZjE@_yaX$p)~??hvMw&~LG7*$1|vY6gEKiw_jx^CH#hy!ARQ0_D<;d%I-mHi=_s!|6r&t&YlKgR(GwV!#N?4CEI<Sdt1iXY&<mDpp!x@es_Co<Ldh>TS09!o+LlGNp<x!}TVRtdT<%{1_%Xdme<ZX_m34AqWyp7r#<DUkc#}^Ioc*Ql?i8h3^7Dkc@**5GbPw&WkeN7eu(g;NBRj!=h8HZ^3E<Dq0^#xxTTPxANd90syX!FS`#(VLC_A&uX4pA9|99gme}gnmGbk)TYvUbp*FaZC;&k5$BGAM7|89ai?)$EHGkmS%P-SMuT(9UI6>$<DloU6Zg`;aIrjVxt)l3rU$v@7=IZ<q!hCEyuniaLWUB&LkO?uFXa-&vRu<OVj6;W{T&u!OJwHS78Y0Es+Fx78g|C&i=ap?(X|eJO@{S`FTBK{I$1R9!wlVEmQrB>tnelD_f7ofp*VZP0Fz)BdKs~gS<@4`rY0|u0<*P{_qaJ5^-A{qRwj;RC;66CEV!lw%JhdYz-$_=SX*avtCF>wCKlAxuIXgr!2m^G_O4ne*fY3z`5l5nzT@^T(#Tiyk<YW9;z@@&j*e9Hme@XKPNTVVBUi=Fo-$U)=gyQrnfkC^oWa&QV&}mXO%&W{=Nn##OA(1}CO4;vNJrX#fgqFJy0sQ2hA?Y4zL~aJDE`QjsULm=mRM?LEduW%+ns2}mVe3Zy+(K4I=#R)YR3FCz%IN>lom7Y<SD#op%-~^lxVsWN+|dJA&QT?bEW{$9rzP--=<AxlmDEB`R{>Y7x=b$?yb?eZ)Kpws6=JlMVJFJXMYiT6VHu{&Z^vFRQdj*WZPZP=%o%N?r)iUj|}};>idoyaKSig$)5yr0)`&o1T<QDiP_9B32lB`CZR+XpJ&g>u-@1<9$Ql3ZihHYquR`Kt~(oTv<3`Toug7}?JTmmY7CGZ21*;MW7<6B@AUD-JD-whXpmFYml+G8S|hc>XhKgbFEe);Gwk^9Wr<O^0iW8aJ*aHv>T*hMy=OFf-caollc^26TaYv{O>Of05M!$ghva0#I&-UK&*gPfxM%H`6K9bvhyR0FwwV^?nwLV}8Gv~npEKRx17liroH^NTw6j)($i4K+0;W9iPuUoB0iT1i6z4R0<~E;_P<r;<XyDB-=vcT^f{8cIQX8zI$>H4$z4eagdO6$UWe)e&vlSI#=I82D)4LcUDSO-u)V%WJ?tt%ry^C2#*}s$HN=LH_sdXC>%`pGi<FJ(6u-5F2oEe=x?|%pOp=?V~{)vmA*>bvH##w<0r+ne$fYN=uW+?MbU=$E4yU^<}7@|>TZ|V-&6WpS5yG%C@=WRFhjUsim<3}hU9X_m01REK;9bw`&r(kXV`e%&&1|R!(Wa?ap1j6;w9ny|y`NP&(7Frm<@@Qn+S7sSb<{4nbJWw;VX3x-BGxFWcD@#i2rK~Y&O3m?gpg|i?N4l;m4_!W#cwV=5G)_W$eS1La)5B#4yEezb_crPCyL*Zdr0Lj?^NfCJG<rT?kF;4>Q`24g)+PRWmdD)kTX<!h{~(L$Mz-%ytx{iN?Rjf;{GG>z2=XGnnZVS5RqetnysS{6h_4M_YL2DuWCH7oJML<YWToY}E^aLA(vvcUrMj3wpE(`UyhiD_w*9<oH|y3erT#vAbR-WtiU&1EKGSWl#?RYQw;k3EW5h-1c5K~6_Zg{0ccz}UH_=WP=&n(*#&3LZeWMjzTntUEm%c9TNw}bHpiX6CYPif>Tg2KVT$DP)p!-@I>-xGi)?0ZivDIX<bxGV<G`LkAs8K)hvCiH^`(xM{<!^l!bEaO>1!*fvVYt2B@nG2HIx0q`P<WV&xSTyUMc1X1XFstA=$3-{(@L8txy){MK_8^;?!fE5h7H;ZOOL^PfAVEO8br%-hx$Pg*E_L*!m?BDd$7?DJ-p|TZ}+o(0^avRc0XCjmfaC-COhF>n#{2GzydI{_E<A^K@nSFO@G8%w2=$Kn7rFpn6n4MBZvp(V=o%8BiJT;BtO(eA!z6>o-O+PTg=l%Ui8Rzv$>q0G3LT6*Jl~Eb6ikrTh;Vhh=Tx%s&e=0`e7Gjs2d~ev-*Z|?y@db>3(0<jVjIeE3+4WbTKS<-SMRxEpkOhQCtbjIGBP=cLl-iwVE$PZ?#sob@u_SR0r5iku?qiy5gbSh-MfSALue<rrVBrBDKJtOY`-G^{rb(DzGwhoDG_&+AW1zRpEXybfYML!VacAWjXJK!9*OUAw{QQaZ3PxuTBrT1|e*S$u+E!LOgvMx1LP?4}YX03G<=sICpVY7YCM-It#k{EOz!HV17GCgxHunQnuji=_K9B?mDCNsgpG`y3=?$48%df1LL5;S<hRKmOU+eFdNlu^U_RLh@4}Ue3s_RBdmu9Fp3`g6c(-^B!?-o^0Q~3?D3^<g7ZUjjGQkJvx%3w*0uExj!+vp1VmKHVd(?t`U`pxy*Kx#WT2>9;`Bv1)fk4d*^WrY8QoSM>Tgr+RD!fVDz|@575;4TOTt^ZM_j?{QYK)$x|<D}j?Zd%pPzP@PBj-c!pMe>CsZ?_Cx>&6Gw*OtQh#X=hgv_xf4X!^?gb#kkr#)4cR6kHtzNbKI(-1UG26&x*1x=i;r334&$KrlgfPQE3XjKPAzRiUT+em0$S??JhN5uvl}v5@@=U&S-J*;xRorV-pmWyLEY_~A+vt?l0=n_Qt9I0tsd(g0pumMU?qwgSF0lS&$$&);S?_wY?X8VDY@#B+BV0+-C$PK_Y-n9+I}r=Vmbr7!)(RbK88Hnj;u3}54TCal`=&$T60dfDAG0GIwLNbbyKOhQ>g<oWB<EWiH(Y!-yeI+h?oYq@?#pM^$qx4U?l*2Tv@;3xju)tv=N`h~2qz}vyC`DWhsm}2hTaftt~2zndj6`vw9AWZ3B~ODlEYcJWZQkUo^Loa4tkb4>N2`B=bR>ry-DJ@lX33!zRnY8d+~h0dzsmXD!kY4!KW_Ele>8{?has|2Sn**+Op2*Y8HyNA^z5`YAJKegUyBA;PQpcoI|l}b5-V*E)7q-VKsCok+`U-LL?~jJ1?sRrZ9`>F<KPMEOG;63F-VHP8PD|H1BNo<&4Fp!#iBG*qjp$;T7!q-JwSdr#$*zN^#l9IF#O6_;4@LxYiy1PpSKPlRw|TZL`C}Ce4#MTb#t{U7lDu+_67$Ip+g;&Zfi2!)Q_w=qr5;p63BUpyt?(y?im7MOcYychlK&wz6qayAO2OT4fk*sVdLQY-rh9nqjzt!TndSy_<gMj=U)82Qgt7jM$f1$8)fav(6Loe;Io+DEF4^35?}Haxy^SXk_m2Fdh{EOlAzX1t%UcOPS93-1{RP(p_xV;+m%KUW@~f16^^?!5_18GPCg03VvG?3Y8-+Ve@ADd$UEXXKf#|6^M7;I^?>`WcPQDHbJ#M%q4{6be9_G${0%@>P*a*dYZfE5@rH{?dv66w3UT`YTm&%P`ksLgP8hJH1(qL(2wFf`TwnF+!S%Dc{fE=i?r(GEBRRiu(;Vlw~kdatPW_X$y$5JUN+n6kRZRf6|Gj!Gd1K`)U-x$IrKsHE@V&>-tO}n(v5505M)w$9K>G!V9eTGE#wooptUC*#UnN7RbmMIS5;~^(C76HYY=;~15mm>Za?5>lQ3l{<;%QV!0*+daHq5K+=x0bqrxC-iA$`{xbjMO3Ny6e3?+1tv%}?so0$<((viv1p5D3^u`W829hl51eW*(qrmnC1lJEms9#|_Q^v>I4i1I^@s6$@b(~rF<LLKUU$*le^@pCwYydXLo8#>*tTp6^`yXHnUsGl-7EoNF*SO09Ek5=HqQgRXixj}Hzq{P`6W3q05PE^0Xf9>`3V?cQah>H#3{gdrGQ-<7<P8(c%xYvW>gC$s|>|MgRM+p;}=V1%nBOLWgcMndsuzh>s&~fw5_)V4;G{Mc7#nSvDv^vpy@Zf>v2=SnLc_n<Gl7Te#D~jN?C5Ee7N(1%6Fv!0=onFK!O2x%6=(s~&+FRRQ&Yh3n<A2Zw+dVx#YwWgI^Kfs!ymz|$eRh1hx6g|IhV<)E(8Dn5fM4O?l(6{wY#yf-hPZuUHwB8k9<pyWx0D^7F-@_&npwdX<r-C!I(uH_%(zL*sMmRbQ;uR{8kTFuRnt6&&ZR9*vrw^o#0(d(dUXzka_xgPaYJi?ig^aR%{guBE(fc#N(sl3*=44=7ZGQmkP{?Ha)uby>P#3i8rAB|5_ZI?WMP<TgP0F8L;Fnie`fb*$TMXK$_BtwBn=-IaIQuMcB@O){3Ei6i*N&Xs|<B~FItKZY=9iZojRhb-l->6ZCbrXut$UOy(<Vh8kmFu=!f1r5rr#qI>WycI6;{^5jm-QcRHnD=!Ci}kXgL9G+9zXH+0K~qV~TUdH9G!QB$C5RZ>l<PCBG+hIJkdvDs^7e&E1rH3=N(=z#;}ZWoQQkJiMSFOSy5D>M`-U!y|uVhw6D>OC8Kazo9Yf62P&`TDq^2SSG|#vXlCF0<C@8GE+h*xNs6<uav;BO<dFPo!#4M1!iu{}#Df`54K&z(|vMT(IA|QT3o^ba}xQmB)qJ{eoB(`FGSFo&?vA3uw}I*5UsJ+`kPU7jQ%h44pV%19;d?;oak1R7z!PS-^BEHI;<h=B_(=T%c`&k^BmFBQiZf4$u>h-(A4sL1m-Bx;NrW__$E7IE6K%^u&z^toOKZ3`JPIvT<3fY|{5yz4Cy5KqC4j4e&cAsvjGbI)i`1TBXL|-*L^UY@*d*GfAme?o*MnOxdig^CB|ELPtX$>4~`4HU;udrJjd;?LNJPa7m5A_Xm~xmjWgDwMhuqjvd&es9!oL;O5H<#TjeB8u@G@Bbpl=0osyTirA=-@njMf)oOCp*M~m9x3W@+3lf^8Bm;lal`Gum6;Nypz3~My%~lnd&mB%7?+jYoA721}f$lht3d{|CmwTi>E)Xtft{<`!YGy6J*NBuZV-!wiqL?rZ?ly%TZVvq}OwKc23_eNn=Fv-wXI<Dy(T7Ufn9w%2u=CV|ou1!i2YbitH~+vKr+WJ{{%51gMk7qCR@O%&6R6fv@iiqc%ox{+$ly;v5ISh}fSDI4qM#>)j3=y!@(Gk+#oag@u6$l9Flk}g`Q}gmpGRvPS|0Gwn+N>dQ@}qnf&ar?;J~86$baLdTEH#8JyJXW^4I_I@3TjSM7m$w8WV&zhg;Zb3_Ul#{W`Q6etxH6U7XizECQYUrxY-8#TS9$lWOATs}9bb3rA3B3UfrkP7-Kwdt6AC-Wu6;q@_njLM4W!R`Pm;h|KO#(kOSDkZsGgoEDCqv(`M?(K+1gruN+MHCtmxbX2$V&0qer2~*7szNUL2O$}Os6RSk4@uVqN;jycxjM{FQB<502h47SXvq0UdOWs7>jwv6%OY{Vt)gZYov<D&RFjh)n^(Ma&9lFq}ZSW#_XWzdLBKEO6nmlB?(@qfGsS%-J+l`3i9Xdz8{TdIF@74*aTiOlC^c@k6PY3>J4Tdin;p4{P39FZPPmex1K4H&K&%fV1YwYgJp+=jcrEV#GQjRKuIodyHF%D##ot^JD_ghW2!k+Fo&ROfcand|KY&H*1PatjYlg1IKcBidppxhlkeb$1sGte1NPu8gTlheJ!eaUMyz4`Hsz#<7$Eq5)Mx?K{~Sr==FYOTVKz3#vr)7hAcSLhChUU;LLHI_qt=U1@EfqAAPreh(ay&5H~l`sj`Y78XwJ2jAq`R(5T=E#tyV9t~c;;v~DBPm<(OW7mkoOIYp49VgSOTm`>2wGrS*jZsscX;WBw#Z8983u8!U{48st#qrarUs=KHWaB;e5hPiY7=yJki1=Q5DY;GJ}#UDBagva%WGFE6-{l*rZ))Pz8{We5}cdxQzV!7=28?6UKe)mLRKU0W~3=`RyfW=c9%qPJ?f?*qPs3^eOy!oHGCnljcGfrpl6HB`3>lhqscUE`?&S7z+*;X=iH0kXzg&^dzUs~vxy=g)r3snd4^vCzvm9$t(g#X*ozKr1XE2Vc{}^j#2*h__UXH{7UGMMem81o^-N|00fWx%*XSLvcHqbF(jLAvmuiO+caFVjbQhlG1`>;7MdFTCSy$zigm)_ZhJY|2u@+4DRfeN^%^G8jF!3>Kc^>Q`X-AYV@^v%Rw<`CIhIdqFZvS&2bdqPczr@{E<|3f>PUIH|N<S>01*1{QDD2c2I<!=)X(%>X&EBa{bg(@Sh7<_|C?Zl)yH2G3Y#}2f#u);JcEDUz)122ybfL=uR&2ue(n3ruT1q#OB?~U@E(&I}lPwG`a%4fzV`rX!?ai1+dJ1ws=W{(ac(MAMU*jvg__t2q*Wo++=0`tewQ_fe1@S~)#H8>dhQwv%9VWW}QOTGif*Gv+3Y{!i2XErs4UhRrd$4GxPZ$va&MIQh7!|_JAl|Suq>;LAQ@rcK&h1yQw;BdWJuy+(`R&gqelN(HFzG4d_4{Q4m^p2J`}b`qfW92R`E}+5wB?)GRT-f@-Bpu^lGxp%vxE^PJT6oVJJ32S;snTH{pA4GHb5S1V29ovRvoabSKkk;b-;_bwdsvmbBY@$FJ}tokexvCt4DmEU$<Rc1lm3CBDJ0vYXA(Azy)>-$%2%Kzd0Stlxqn<Xn=O)IxAy(n<wuaqqyJmB3KMq@o9~n!yf*r!;TgmZ&L{A?b5C()hypjQLDS|co4+A*(2WUd1*ni=d2w<TxdRVbB@S$M`bj+EGTF;a|DgS1|VFaS|vs$AfE?}Dk#KfRj{@K(Um(X^Wugf%2NC5i|@1mU|Y2R&7b`{b~wKDLb9{MLV;tp#&&}+fHC{L#=iN}pR&)L(t@kT@7?f>g5DG+=xCHbHt#A-p$RGZDj=>#3_k8EuXI=&9M;CW!*V!Y&ila2;dnXk1Ft&AtDc9~LbC~#`e+(@i-=;QVjni>ZL-Z~v&SO)gL;L>vE{eyp3ym;3~F0Ea50_+yJkOR=N=RqjY_ax5QiD8Iq>`OtQ~`X==|+&8L;IxKa@mEd_09^qlXK~IQFnx*sI&0LARhsi|iX>SOA8iLxW63Xuuw`^$H!jEW3rsnYZ(}P?8sSgpUh;6qu&ZNgI=P4x6X2v+IQ@6=7OeZ-2Is(mtm(7{rd<9Hs3v;V*+7^)!kDPz&#Gyq^XKFqC$Kl!l`lP*i3ZROq3T)5Dx0Fy@nsXAiyUsND@fsg;NIJoGKdv#c4Gg3%p{*q84DB!s@V@yy(d-vvzUPuksqJL-GkJTSj+OP~}MD&*yzH$%9aYey)mfLEr(D`Du}{sJdNV;uYCPsY%X?lfk_>r&2^h=(!~Z5creQ)n61*zVwUneQg4ePL~-2#1{jH&i0l;aUb1y?c5f#Pk8NWN^ZAvGvE?-Vt_*Sya2sQrNlv=BpnwukV4@9&ED}*yvU9P#KcHvXU2E>u5FL1Jb^zEx6KI)toyncIy>T6?@(UW;woQ+Z?#i?^X6}+JV34UKiG3FQPaauyA-|;AhqkNUKEC8EgPb3^oVcnW6a9Da}~?<eA#Hxa!ICx`SyLK!50{PMF9V!`ok7`oZ0eTeB5>^n0Q+Ilh-D%-r+|H6E(8Me&_){^~y|)g5+O#p56j{Wo*WSgFQwS5nB{@M&#QDQb~#5nww9?Opmkx3q*|i67D-vQJL;K4WK%ll?5a5aEdU;VGS>&T`hG`wLi$-bFxyAotoa875o)gbYQ<L9mCygJ0tMJWEmHYye+H_i$nG$iinczwkxKkafX?PBn$|&e%2x5{BFd04*PcU9oxlH3)|QaO1V-f)(y#HeBI7w(G+hFob!11Zva5Fnb`8T+4nyP<#B?oB_Ifta!42+yHt4TL<Cd2={_%2loRR&;k73bTR~uc424(?>Y?#6M?4Jv3u#FC(SeO8t^>B`!$Q>`P#d=a&OYWMf%RU8(k1v?GD^aG*a&!p5y_yeMuHr#)4~u^LqX$T6T(MXdyE!C42~ccjU#OSmkWY=haX2#MuC>F82CESF)Q0w%5iy*gj73_Jesq<p5@Q-7HJA8Qtcs%-XLm24G$XGk7H>!{zY+>{UR7n}XX~0?kO$*<3PTTV29<kGm*byU~HbrwuEHe-2^$T?Bk{Wbv{}YD!HNtbnbj)YP@i`pYV)IVx)Ah-LFBA@^aK6q;CIYR>_{4G-^!MY&e`d&i|Ap@qBe;1%~ggH8WXd|LyoJ1#7LAC^}I4!^hTD)D<i9Gk6d@ixj4@ZiGgR%!vqvqobx0nplX0NDyaAuO(ZK0_HuLF2dn(f~#J&J#ECSn>16)g^%rGC`sRXoMRb`2Ueho;JB^OQvoyb2fAGzMDjlFy7y?rEO2&RW2+z-G{10obt4nM1}4c>XBg;wo;Q|sa=8w@s8UBGDex0lGx?xJA@Ko*!6FJvA9Bi<#nWNOGAcC?Ec6V^3CnJtoYpPEUqdiy>1VJp_kPNPv@I>CU+%XgydGc_+@nGY}tfe$rMc4x+Rh&9{AnY7<yqj<x=$X!!FwvUE5vQ)WyqBRU6C#N`CINoohnaJ3st%|Ae~*KXsO|BXC2<auog6tO#VC%Qhr93mOv0N9Ye`gg=-OzGX8)!gn9gh(Nv*cQzp;wU;#@Q0IjCU;)8T4c)<{K+Sw$g971pcXNVX{e2q~oIe;7V1q_X@cU^>NKpHb%z1Y+f~x)@j0nyjj0h%={@$7p4D8+yr&`Bmo7FAz#BAm*sJaLxsQczoJOA?6|M9<xi(}g00r1a1XT{sUbexKF`?LGxW|Qq~m81Us!LadR3>ze0-pQ<CK=?354d;I}qXx0;A50p*8<PeRe^G-5aqnHs8C-G5G-ljoV~{(u-qn<m3FN&RGBSS}Atl5$Wf@iir}ysuNo)UHU5nnVvV*fGzTEbF|H;!Mhkbgu|NQLq94|m0AMT!?mYavipByz>=w<PwaW0-U#hcRQ<Nf9{c69p5*?#WDXgz{m=9OqIuAF`+T0}#~F;_2cBEk4K+nop&k@69Siux3qgKc>aFVi&#6qe`o(hGq%qO^-pf`R@_r|A`B`bNsfB@H(kNW@+~E{wcr;F(h6a?%#5+_ff&hSCc%om?{8vm2ryNuk}4NCidUFa9e#_9D8cbvPoY=G*`L4$bxbxc%CX?e=6cH290ZW#9K>Y_H`-v39R1ze%b6V01qIuu~x$4b`432JQXyztFG_-0{VNZS?V3!l*EFAd{Z)!Z2h%$M+0xe*v6W-&?SyE08?%x<X}kzWEP7gEeG0aMO@8o#v3sc|?DDUdn!HkwV<K9e;=cQSrS+gW+9NXEd~uR~Y3}uet7U#w&=KE^+#$ooTNv;tlP(;e{(5-$X}ed3amz?iKX*_2&xl^7-lab6x22JHapO=BhKvTXwTG8U4+?g5CEnst35UhZPp%rHxASZucR$Zm*C5{j#vLzLj|ucJ6(?_tF;>hAo(5-ni?#Lv|1^(v^Ok)0Iu9vcXP%XMMqox%4VEI|vu*N0`$O2g7*%?)u>tcJ@b;>2<&w*VG$#q29PTy{T5J3w9>|hCB%f{(2$#Dyyxz{-U9U_6c5vEkfI+8E}mk|1`H~BRNBy>^$;iVdEh{r7&vIuK%c7?QU(<QMvGUzWHDO@AZwG3$#lE?)N+OYLx?C-}vT7KiPPXpzA#e`s0iEVK(HHnn;U)y{tT;T{G98c0oH0T@`<3hRP&@<rWrJC!j+5attK$+c9Te7)?-hymXgVR0y(dVL-^5fk6+=RJvOW{V*8EsWy1(&H;XqF_&NMzGE9AI*ZkYh-5?2#un5S#GrC@;d8bN%TZJok+0b9(4S0je~&Ly&KhG8>^NIPQ1S(~@Kn^j_Du~-zCEp2Sj6p@&mE{(U@fxY0iJ8@GqyX8+1b#=)4^~4&#!Rv4;tm?8Qg6K+v!plyVGR(q2Tm<Hzo~>A+BZx3@D1X)iKb{<3bH462qtT@EVTXOjj+_qt)9~TV&lBPe-b&JW|^_+UB&U5XB=6puhC{89lNi_W%J0?y#>}G5CXjg`JJ+ALnvH7F+Ox?)|;P-9~GFFTJz-m>nH{x(_9eT8(ytN5`UFAa3~*7BQ?p_H(9%Y(^4Kfaa=~>NU?fcN?%A?(*jaFG?PxyuWUR$$LO|m<7`TkKN$ms5?b#VH1Ogm4M~`w}0eGi`{uZq<Vfh^E!1BMag9M-RF2cdiOafjL+FOfBOF}aa&F!o%V?7tm`V`8B&lUXUCaqkQKTL2W>K1bS~A@T#{3%ig8lKWU8fOR2kFBZcM)XnK7jFyeI~Vf$~dVqFJ6=ragGnj=CWp<jGJTzx~H=zWVWk)TBGb%gUzurbf_w>6ArKv%MK4UFT-8{Kz2-%+++52PvsI1qqol??|~;*eTZ*4#Y7FQnlg$Ecp9Apb@Z@_XG_3xRTq)rLWA*lctNXZjZl4UD#>#U9{1xvBo3}uKkh6cwEWiZ-45Rw&$+1B=Hbd+0Eu=!C>^>K<!}`cbD=0v*2*2Qq@?zs_{5w%vgl85ShW|o1D%0#mUUO;aQ@c;F~e?tWnnj&SJ54&lQ>)Q!OpKPB%Y0*?o3?dUE(VEY;5rpFS(^ogL0JyK0*z?Zpg*vYwW`Nb8T?=C0J*BeC<$KvYy3g8t>NfBNU_XgYDR4?U0R%D6BO9jU-l%3L|iRKziPMSBpu^)E5Bo*&KLXYYLTSO3?nJ+sygfY&B?g`Gn*n;-0--~RiP-9z;L0v+ko#_|41>lD<c*8Xm*v3HuikzUGBHBTMN=0Z-8H$gBGu|sMLUiY5~=RUxx+<$jSPGz&O1Apd0Qh|#3i>TtgmyDSw6si5|30?!nATzuuG8ny04T{`f{PO~F{_LMAZr2`owIbUmClq?gf{ez$xn9-6@o#SFrx$lRxH+e=wDQ~r<BT61wm>8t?SrzuyN{7=4?a0MVta>;rzfY)*5PiGo$rgIoYV8&M)T-!cmJI2|A5jK3uP;!J}n!|may|<)(T+qpl=)+s1Io!X$9dIQ*UOp5?SY44ppL>-8l$`Xt~B-aPcIN=GUPYozTW<AX;w#hr9qWsq)u1?QSrdc;kqkoLjV-H}ob0cO19zogEc(V!_IMciQgxQB3}fLBEeH+Jd!7O#m_?rP|}s!cj4I13aS|Ku_^h1J(wA?0Fb;5LgCzNPpNkpKE$asc)5S^mdKd+4e#=dqLw56)$-Bar=|j;qmFR+n@AX$VO){yNx}<7bRVEk~nwYU>pE+^c7KE_+;20Uj{>bcF>!-kf~RcXB@exN04V*#QE#PCc3ZN-XubOmI9GpdST=a*>C@Q`?r5L&mP{pEJIaIYvfN9<65_|bqBltJ9nak8e=!;gg#e^xP=`1^7jk&rIYGQ^={`z@7$LQ^p4@&(!y9x)Qztf?8e3K#gGgG;3}n%HYh^P0v*6=Hu?`L^^MHU#^NCgmz=$QJdxiYcU}M5TV=G6$rl4au8wYhj`5X$xAPW{NcUikx&0eFS7hq6bO9P`=cJOvbV9l)jo)W4hM`at*zxVJ#uXmZELx-!!!TpI*4BRqorv*@5Z7&*?(MJ8=WNF1AgvEj(e487<k`t@{^48iL^v5a7(6_7c`zx_lQs6KH>@ns7pk8UJkXtNBjX2~y7a0LY&4b2j(S+ZMOE~7J86T<L19Na-OP&gZ4npiWvopYCiuv|4878~%`I2%aENbLxS`jBZAo)_0m^32U1Z|&swn})hCwiizV&`w#CU8Pp@V+Q8%+YXAH|EXJ65#&@Netu>;l7ytvhI<`?mYiK?k|pABUdH#xD7;Ezl3Fl$y0Q=k{ltTkp8!DuvvSqNx{^hp<?wru4L(1p|BT)7v_%<%Snt4BHy*sTc7+83x2F@8U}x7t@eGGM>NJ5s#gB`xoEpR);s+p1i)m>C+8j5A`D<ZMlwd0I26}cV-L8oO`c}x{wRpVxlkzDuzp%H@@`U5atKZb;IrKO_=FIE~qO&E#^ROxnfUTKLn9JabYMek5GW##%z*6tVw0?rsf$s5Cm+pMlPHF$j`r6YBxq#rrW`Ic$02P#C2;-U>h2#&~7}G*h0|Ji#Z!MkKZOBizv^eJS+qky+=V^N_&<fXmTsf@+f7+rWXh3vcAITmWP9V3h?Lo?JqB;E}dm8jKg#|Y)4Z+_EH#N7VTtSO~(|fax@u2%P>wbYAfui+i^ob4x*f<vfSlo2pfatOdl#e2BeN8CbSb~GFm?iBEJhbxyFDqPa7o`3C@dHHyE)IwmgDFls+hfM<9b&*@T!fVpx>*ac+lDX2kl_NLU7Xr1Vx6KZ8xKt69h76tJ|OaXCIu0!T-T0gPXn-u~Ji2jR#aKFkR{N|Khx9xXRsO(P(;Ca{uMtXOgVn;-pT6MIc6!ies9xX5HrZ^FRuW$P?U+=9!DOv=$)JT&Q&x8O2vz%6i%KtGmxjvmD1T;GIE<m(&O;D+M^{-n2d79}3}7PuKNhwH{-^ZWn}{{t_S4r06(isW&x4Z|nh+wJqfoqzf3zxq+eYLoROB*Bt^_W9~SyzL5y`9OO!H1)`2`W#PVY%zuD;Yj;<Hq}q7i(>JrkNS94_J90yHu5;xsmQ)q%~+*=d?2t~z}+mj-6$SnyFdBg^V_8&NxRL~(NgVduRj_H1h9Ct`}DF|@^)({^zl_#n4V-p<&DzLj<Eb{?s+O_wA4uo{=k<5lV=7|ssk!)FX+BD7~A0JS=`LhPupidE4dhR+nz&PlWRuTJGI-MjxHkeX2AR9e(M>?`CPv|$8%QBepGaE{^g8056T_6F^l`OS4t(<Nx`WW_c(A9C+I|8>xulqDsJYNk5&1X$Oyp@wG$N_{87{m{RyZQ#r|~6rEihHz>aU8;fvfpXr~X6!=Zms%$}T{w%TWn&yG$Td+af5xA7pbjiGMZ&DJM-ho@~S@xA8hNxS_}RXaM}Z5-`4p@t5iG7MnL;ze4y#>vx98c#Dyiic#WtiqMA&%nm`&TNsiu#$KHp2G{>D}dCD@%V@5vmgGD6$+&aB#nyj5gY|qUbqXoAN-0YK%QcuQYgKszN~~Ey_8s7Yp-3bvO>8~dPt!CJ}Z6%kV`D|;%PW$g$dFqX*C+)?(8wPE<u(FBrhatslHaCVC1O*C|*MsWSQ$q7sbfq$B#MChwN>MeOENF%?jSQz#pw=4Ae=`EXGrJC?DMg491{#J`|Z492>|WbI(24(nPT+w90^w;w10Vr$^-;vvLiyj4Dn17<UnV6@ka$4PcyVn+CTD+BN*FfF61nd!r(E?cuj-<=em|=oRatZ#pZsq4RGQJM8U0b<T;=j@@`rIXi^CS8c0WsU{o)*$xzgB9wtqba>IENbC7&8>&9WS4P;qBp(W_ts!mS(|;UZt%45=1>)gV5QlU>lQlu_8o{=fod}-goAP3<TK!`zhL@~Bxf`&E3RWgJr4N7~C&;Ibqr*KuX<MJ2(PVqU-=70Em#@Lm*W|Ibmk+J#&-RZFf6#u`IN9U%`N=-iqDzmd;!jS`_qEn2S`!rJ(UstfjFg05Wn3dd;Tk_g+?f>A^ZniZX0zQq+!JuoMIXwGoBRCRAYJbWeINEu4o{x8@!@Ad0lJJ0b+n7s*dO~IbP8JY@VLEq2)Ll@Gl$i^!m3^PNR{UP675#w{3*U4jHRvpJ=D}U;qWurHNy{MtBb#rZRbl(RDZA8-rGNDd~$?R^t^G5O>x=CS*(p`oOq*|)mAAP50*iuXqQSayfKh~G6@6ROF#+EDwM1qF``End0P6}8_2B6T<dYNZC1Ck@R=@XMDP=381LZ#zN#tnVUKNk2!-cZ&vk6GYQ@>$S*b@jFtaY|rJmNn%<86S4)=Y=lLgx#{idGmxA_DD)y&Ltv@Fe$15;}P$+W)))p2-ko?8Z%S(g;Z^S;m;w|p#!fC6J;z-_@XKo@+J3-Sde0B;!=Zd;qYdY*PQeVc7axFS;zaz)*CWVRKW3NtrUT`M+}#&jw#saQ+$FzycUGl&&nt-d>qJUz$2w6<<mQ{j4yPKYoW*)T;WUXB9dkVrCf%mz18V3R&*$Y^p1W*yB#F0e$t9s3}!auR%Cn{DRh+k;2N-X@|T#Ta!bi!p?F&t;3PcVUaoe7301WQ+AXutg%kz9qJBoEdCUuWaPAMQXwN@Eo#batQi|hZB7YlE=7;p}}Z<<dRG`v_poy6ee=FD^4>!VR_@C7qwqn^wg%H=XsOeA?O#ypz}&@2ZTP2`;rR425q0dMzk~V`!`g!#C2&M7;LXblY?R4#<+c01>pTp@pBlgvVkw5<BkA1KIo$<nACMpJb+3r><MARArn#4)_=p~@cRDP>*<NGJCW$}*7U7K9~SYG>8Rs{h>yM@;i(lrIsnNX!+xTa2}UH55<GIRi`WtV!ygw1{wnL|lHqXtKMfJ+2MI3(kwK6+cmiG1$*~9-6f&0*ldRHX>O@l5?iBVJHi1t#Q2uk<=wB98&gzAd65L|13bceWnfu{~q9lTgI24?6G@9afP5*I&F1E?fK<hBp%K%66QLj_gf8f0f4IDmmmi$a$6A%vktv<X7MeMQL9RwgjOlEe6L+E*L)-b*!2}KJP9~l1nv|o%$YzMZ`svpr3eNdJUe6s3E(7P#y?iGHn!h$>^qnv38>EP+sW0i@7Ol=S<T<J4R8DSS{N#N|`kC`BfOyNV*d4;E#$dxi36oj|NWV7@IB~hRS{^IN^;V8dvt}<u6TFOu=)bL?Vl`d*)zwLczDPIlIq`U&E70_WD$+*0M{syW+X@(k;1zj(pgE!O5v}wVYR+9!&ijW1~$``;>sem&;b~ZHBQ(BY-*~%A?Q>mn{v-N5kaxTtRz6n{!*|BjpG&muY5u%nZplK<kTrJPS%gWav8L6mk!Zx;Q;iajF8E{pu231P~Dz36E9i**WYP~hH1VA&fl&OUpb4klFLGYBc#icY$f3>=tE@HMZkDw_PI0wGTLa9_Dt1)3y`m;e3D_4L`rDj`|O8JVng}q%sw3AM*RUC^ga`bjXzGjw5_eIaELt9&=g_M7*FEh&KG-=6Hlz24ud^t=neqO&%p*_53XfSG^DQVBUDB_-B6zL22M?47^JF#qugpZ6>ORP}Bt}K_n3$%?ZX5bYo$_%zD&0r~Os-}-32vQudWV#*kTce+7#j=sDavK?$Z8-DJPzcE692Mz&LRSEK(3{kXpS{$Z%Y4=nuPyKDpydPx5h=ziA}5R~Mbn({=t86mZ3z!CjI$G50LKDUQ9_0B>rt&zh4y~MDo%pZ!|!A%7&+EWY2Q>0$Yjm3X-s`>sC)X4)Obrknl03t5-JBlX+Nr**R|Q4WjnQirHdfctkl{%!mk_al5KspS0<bDdg-Ku4Na)raBI*o$w(maU#UX`1<W$`S_m4s2-He&NF{T0>}(^k1<}k#kah~$RMBpfz)YE!EudCDLQN%AE43<Dmy%U3ZJM^%IlBac&Pe3?9bmqpfM=MtE#RpV2s|SZF9UIPEFp51X*|(T(%D4lRH`-+Y-4(A8khz6B(T%UTpO)cwyJrcoq3?04A4$CXv3Iq>-|X{0yKVdg5v3g0+n?DU_ne5LBLt5xRD@S>q!IoX9!j^c?Get{5;tujk{-@NZ8XSuOv;R{LFHV#-y$jGIhpbwPodF3#lYNn>GwdEe=T1J8@zm$|c63ZzX-T$*Y8Ua<Nerlr7alTcl%o^_A~Obu2Brt0A0?JPAij$U59ixW}~H8i0*F;u13<>m1Y+BpJ3|OP1IrlsK_7Y%THw9QivHcGx^+PVN5v8e6098+CSw*IK8sN5(|<F@_Srn~cFUl;{0LUleJN(BAlAj{KE|C>uK%7u_LD+H<#OS;xuh33E!zFEjZ)t#SfD(6PM31TLglme7<%Ru%!3j(=s39^>@N)51sYbptU#XOqfC;=Tcx)x7cpUKHJ12+u_ImcX%=ZLsS~hmvk5jEi;h3K4iodz~xV?80~!VOp^jTuY%`m;SAxh!KU~f+USR)r736?8&kRtLYAqzlub4#mq02baS8y)x9o4=WEVtRx4Cg*2Y)vi%1@yymjE?5vx1!xw2wYC6?e72PkR?9p6JsXDoRFJ~`&PjgtVl9oT<(uoHu!MLg>z)(JiLwFxeE2--as>i{5?*MgNQs}{!WK-Vh3Weq@>nPcxdZa}WY4-4zSdA?*gUg{n()<d-@!cZnfcOEMSEU7Wz!^BAhqoxWNFl1qZlSv^&E{8;h30N_<WyO}))V&rgy@QrC6EtEBOFM-TSY=^nl}#f5i9RF4+zF?0!;Z@2E>j`=Lpa7pEr=RALzZdrQT#~1!VU~lD0z|B<MKq-bOB5eL6wXxanfuN+vTigO0V2ws+K?D6gUaSXA~K-2OG(jSbM^Aug?h+_BnA@@rD{yYMT4yNZhV^ya1&W=#t<GMJ1e_q#4o47fC%)=%ulxJ_>aDhJBI{sD~&b%g&e-j;P{%tdD|hgrPbxK^og5bxOwN&-yAhReG7o;2|~)<&u<vPkxZRd-)=1y_zYKMt(1uZvcD+j~fkXF|U&VL7xUYTE7Tc$Ty}f;j0pjdH7<O?*H8OhdPZpsVtTSRUOzG^}sXN51)Dg#!|kqj9Hu<DEMqUk0_^)f5(g6J?{bv=NZaU#Q|F=E-T)Xj+fSae}a$m$)ywKt*9yOFk;M3pvWY#au|zw3#oeoLP0<?YSO$u;h0Y{3>qmZa>CJ0>SZDh%Nfb%lhpcll0u%6TO2HxPgppCpb$@sv=&D^fpAayrrJ`IO6YV{b<An(kIkZxkW&<dqbh0(%2ukAZ)%*t{ApA=Z_|OjaVVRf8%bw2rz6M)5Gzp706TDZ(K<ktO$&-afTWOR5HWyVAN%8)F8;{qB%3G;nE+_q)99pqH^_s)ocX|<8NhUCoP2591^aH&!X(2ML487tXFAis*0~FOhr@R=;hO`cxaI1c+~X7OSrH3w!tfw>uW_ue0q`1)ewy*G_<Tuk2TXb!&1UEXtt)*7UCp0DSC&4!xoS@-1X8kQcvY<^BOGL6=zH3{T+<pbaMW8PE2E3Mf=RwP!fZIaLcVc1*QQAsUO6(`QQ3Na&BEK@nb5Iv9V54cmBX6ePct8@hmM)Aiz48xGrW07t<-okhO9bvuag1~G&g&#D6aWY3sE5)i{^Gn^4@h#XF%M6PIOxtZkTvMDT!HG)SP6PzVw!zc`ZBdzh&NE#W#wOni8jIhiYI=P7IFj;uRf>&r#vPrV#;!cnIQWC7Fm1t?~|)ceL`3RbD?&@_Lqlu3?qY$tte!Kx8RjSES4@!`Pbh9$+|2!*EO(Vc$YyYZY0&ObA*fopecumvpSj>ejey3{m(kf}h>B&~*d^XHf|D5DHC|rc`x{Y8fqf5%zq>o(KDY#6T4k|MY8I5v?U#9t)r|8=%7hItUQ|^c@b+$pPrr_*T94qWTh;w4r|1URt!`8ICBYe%4;vE7wubeSJPaLqw5Qf6nJCeD&r`TvjHOyd{f(EV^ik7OfTQkY~^-Wd{)eij?H-qr3%4v}=LlZz~vkJ(nONd672w)nsL$HVn-7+>x;bmq@Kjn3hN&h3^?gI7I~`IgK+;y+J3FMYQsGh|6zefEL29_%L-z!@$go24@2|@<0zy)Mzqy6_ZO`Z=9UNTijCcgGsR&S=BQ_x3?|#E33M_tv%+I)K<XEjkVlXI`>M?zS8nX?eR9wRrNE5pDlGlQ`?4r>X!q*l)L&kfFW{+ZCg3OvkteKcOXK!sx^O%kJ`5}W^h))ga_2=A+9~!LV-|-;fS;+I3%D5auS+@WS?k!sV+hbU%dpDb$F)tpCfE4p5vg6-o0UWibYZVO-gGSHTFm-{AAQ!*IL8n4RHoZM4b*b2v<S)8huF8g|4(x=y76XcC<`9+tl-1EsqXW^~}DOsWv#G8ep!Y1}ln|O}TpQ7>xzGf0%%fE|Ylw@LpnJSklcNn65=2X06`in;&8uO~cRE098gmy-((Rl5ZWzPs}5CQS7aGz?J49C!dF$rFh86<RM4!kh1^}IScWSGmD3u89e07;vpxOhY)ieHIs)ZSFfGHLpf!#dB~Z~L(T#`<Ye=ZTtb%Rpgeakg5A0T*+&*EkXXex$D>t(`W#{459%6MS@5S^Js9^kL6llI6HhmU%QVeJ3s0q#eO`bl0b}7>j(J8S!gRlxcXAc^7kGhskX}FW+-Dols*Un*_Q@_{qNQKKRr`O?{cQrk$U_ot{^7$gr4t(WIP`mo0W4+fL*>QjUwR-qQ-9cN`Zx$=?mP>IfUEE*FHVrm0ibmStb}_K7h@bnXI^+PbjPnzmBHuo4#%)NMpSjnChq&G8t*lKzWlocj|@?4n}1I`sK05Ud_lUUja6idq<XNBr|gg-BYv1;|D$|Of5^5j>V`<I#yG#ma>hC|@l)?C31#lzse~z|Oa=Q1cmKbr7}Cnz9jP*=)G~Owl>o|-Ee7^u8hTwvT~9Fv`ys0u%Iz4`ShRHWToC7`HFx?9M3E5^fb)Q8829=i=JO6E1^{^qK?f3MR@9=MZ;~iSD)Qo#-OylTlnPaK6wD8vBRcJ&BR1<e!@X|0eeci!3zNB8sXJm*h(1-gEfgbG7QHA@4(=Q|me$EEY#>uW36E6^cO8S00uuJkPHwD9ZYV3zN#TTy_Suvpx3&uVRPCr`?e{myK(s13OIlP^kJc>2%ncP;@RO5r%br1ls#!B&D&^WgLU;Doch>nKUJ$3A^B5oITt{xDbqnApK~_S|PePo$3SS8A@HIJdWqOi%8k!uVE^ri!ttRv`1<fEhAP+)|;U#A(aFevVp<>>3!Mwz{sv(+v-vd$_Jk!w+GLeB421r}(aIuvI&IE<EF#)-bZ248Ql5G_emGzO~07{nI$(br!t!!<QX^=#ZA^ov>6NA{`epyu5(QAK~6}4Y$vJkG+*7_eIm>!gz!6^2{MbJMsR;|8Jg?k!mnZqsc;5vtDI)f5jm=7r#s4+vzJv5PI+CUIk)9wKnoV#Y@Zb=v7y9kx$7@)8lgkvvE#4Mq;g9@1D-ovYqfQLr0h@3t;5VJRqFdUt`s{$otqAg@(YC|{aaPeQtcKk^ir=eb9#Uia_uz;C{p;cPpN+pXrIj9m&83HZ@7-w-rE+$uu`~o-E8)4|)P_s6v7b=}~G>_Sthx1beh8=`aKsNVL(yAUKgDZttu{a%C^P>tR@Ra_oNWn3+{EaR(Vv4FrGEQfkY=Ryy{FhkkQlqAxp)uQK*0SMVy8aMm(9pZFPM7esU+5lXZT499>|yKza1dj<d`e`VlCdeS>eCWW%b|t?C2nq6iPq2p$bD|GOXl>7j*DJ?%5i&vItK?%Zlf>LFh7}0hyk$%AUe@PgiW;&RYs#YpnAjXt!WTm94xH>TpV#hjzf<dr*d)_ZXV+R|CCC0i#U5=wK~=vNfMH+$RV{>3GxDYVcDpAS{jt7Os3JGSWX&%wxJMD4*OX%3jOZr$}fDD%h*{1jwB9nssYPPf4k63H6g1RV8GQ=-=@2zgpg55dOoP4r2Wn+Fc*~37b!sUNwq|OGQA(uBwCX8dc9d=ugWPVvkDmoa4f!!e`tq+<{b1~>Ti>t8M>H|WgMYBIeHH{d&0Z;_i!T~Pf+H(SMz}}$zv==FwyaCGOQr!hu-+YLW3TVc`Q-Ar&lyQFf!Lks%^A;Gq)VY-HSsRDNp0b*PJ6?14oMOD|?+@V{uClY8{?3i70mW*z1zE<rVfd3H23+`U;@xePge5(7H#1Y+yx_?ZvB?53O>cASw)ik$WAzfWFakE5$Hv%t}d-n{*NKV$zC0{>sWj(*|fxjO%C{{;dMAZTPp!#0^)X^Qzv@ZT$zIJcPHHK)esRljunhddVch+xWZvi&gI4OMx2_>mp~xCg;#q=3U33yDPn!>?zg39hCqFQ%QVFA{F2{8im8t;+V+dKl~w8=fN<bh}s&;z>aFaVtA*lTPUVXEKus)RD;*EdTJ^+e6L{Ouie}Q7BaH*NCvo++e9)gCxX*X%yUpsQZ`H<_jBn*kJy;|iR@WBT42VibJDE!Vw9=;y4IxhaZ-*<{Z;pnrin4Wu<SPIVP<&uX(eb2gcAp7^6)#Fp+GW(47#Q>i3**Vp6wX_VGr-YTbnr~Cbpr`S&m~y&<N5+v3RLui-{YM)3HDpR&do`QZ5U79Z}(bj6~UyrgdYVPiXRX)`)l-64q`k?QW077lCWm&|A<YpD%?Pj<O-}R1Vfxf-SjOASr;MEz`pU;ObSKYZ5c(rkX7pA5K8jd82f1Xolb8;8L|BudCOPbF4oMf)JSycXCO)c-196+#|myRwjhD!tdGKv+E_bLhDWp%w&oDnlVR!cQ|al&G$la5k)jj^l;Y?yJ;E<Pc}q0)qOk<dv4h>X(}P8Ro%9Wsd7eT1WVa;WUY)TrQ;QS5ynN!y@Vq!>I308R`>X42E0}<(YvY5m5e5C1aSVj!nm<XFcy8J8eG*NhN7B5p;em{Qn-{<%@o#gP4~ujI9{uw$y8y-DhyrDEn7GIQ<B?6s=&Hgpk~T4WLDUt0Dd2TOe?}8_~DomO)@TF@KDQ;e5(e7V`@@=RS`JxT*rx#mU{{xq<};RdT3%J8^yMCWJGrxhKszm80kGx@-Y_j^Z{r!RXWm4EYO6u9#oD0CI(!ChGzBPF%FDI(e-SKmhVc^@}e}&YE{lSQwV8dNaX9HC|NpEfbSsJmQayVRRu}5&DZ1)dIz>%VY@@$8^`6Q-!q@x)gRpbm>uD(ymS|KIOIXb*Vxf%gEjFD*ziMMfE8D5IGT;IJG_bfDA{+?b9r89DevlX3~hU*7n*%BCi_;5q3Au)6}_x7z=%)u`ImXShP!fWTku(@zU0=ew(c{}hi$0&$HcA)bjEqI4Kx2(nS16YKxdS+fzCP>H-XM5>B@p>Kf8za-2p0>@80(?<?^p%o8xYjz6g+@om<7a5@FniD1+(({~3A+Pss6BbyxXOO2)m6=bZm}8$0CR|KP#ahAH&bJ<hAt9j2?){iWv_te+H9*R!5$+z&#bK{wezevCa9^yOng9SqVL0j2>+nurz8@T>rB!T9WM$-2WJoEOSCFkGr$*|!)(5gdiA68qygyx}KeS`lTGHuNXqEkODm_s#0i_m1Vk9_?TIv3AOq38h9*$V;$8-#d85Qf7HwX~u3C+cyZXbE`=wEG))7eeIOQSXKBL#eup<-Z*tINKne6dCRK)B-XU4d&>Vtw;kpC+!&2}lSl>yK&X6Ehi6a%t2InEPN0;Z1igh#PE+cZ8@Iw_xmyYC-SSuCSFDUA3psI7G6kMHnaPP$ESmVxFh0q1BG+j)F4^R03Dc&c%!<S#nLzvUHYf`w9{LKyjFI<SU}07Un<#zX&sZABc)Fsm0k*w&LU*&2aRhmEEe*rqzUMXdKnG`Oldn=Mp6QR6aY6if%F#Z0?r3c|*=-~%<sDjp@q8i)3L9f2Lz%jUf1Q%JI%M56>Fo|fel@I&=fPR-{=ATr6cX11%zL~p-eZ8}sPBd1d6r@#uO1}=kenpyIya#Ssi?%zP9g|bQbqL^U%8`^heD(10(@R%rqeoay1LFA)T#9dLljl3TRcY+MWk-%sZNq=`f3?H7pS3W%p!|*jRGJh#Z&tj)7gPb0}bs}IehX<a)k%x+xPK-bXTao^*weFgy!Vp0fzW>QY+-p!&EVfmLV#L@gRSHgHI+S4oyS^vhwI!4Hj9;sZTn_r{2&oZSv`e^-wfzl1P<ZJZK~3*@<@*1AuMTs<9U*_eL+#fCS_BV)U|vFY{EZIOpglT3C}Fzrrku4q^BTPL<z0<vlE=56G{~DbYv!b-yKU?3p(;QKUX`hsbn2OALR+r96M)2H7J~>v6fka509vVV}Z@7yy;{maRY0#{3L75pKsH`tgkhCb%5%%dJLphH#orFh){z;(0y7T2$F#>-Q}`A#Z~3$<cP@2Z=x<nIONT5UEx3>wRXvh9vGBk+x#R2I&1D3AQeFNPvH@eNA)HajZrl>$B_%H`x{XehkYLcG&FKqsP4Qk3Y5$=NX?FLKNh3ZFhv$oMN(8(tTI@lUl#m7-zVLCJZMH!;ya$f)NMtr@@dz5k5pkiQ9^7!CWz-_&K@oKc(p{tKY*wuNZC!?SoeNmOt{2O<%e#BVxS<li+Nai`4KcJwQVcRa)QZXlC8KL+o{*<8$SfFRzk~n+6InXSa+6Mmb>)uebxEF1qOjY|Xm@EkRr&Yc7&hh##IO=99>~^e~hbz9<2o{NXC?Xc5v|=Z#Mr$NML(Q+B++d;8VN;qK`++k-{v_HV{r-(|2$g&tkS3WJFK_NOizP5n4vWA6gw<E6`jDRc2EM!>vl3@7Yg2JD+3{ZzbF3!NDHJ#X}p*06_9TtI8j8qiwfh<&ede0+HFberwclE~zeNUg<zY6~>8P&MMI3nJ7SSG&4sHR*XD6{I!D^hM(i$jM^21pThuaBR~~uA8@iOO)z)JdAwLi$Rfed+s*lSmP78_!w~L(Yu<gF^>K6C*pDr!x!z4hEseO7rMyCxBoQqLjAp8n|7#tl)HWiI;pv`^QJNUHIHk}n>O2PQm_PSHH6yT&_krjU!5DqDk<t|mqHRfQ{FC8%LM6$GW8uv+vs`23-|UH;<4bd3$oXL!-}#OrENCg>qwfs*fn}+GxYjF2rxn*>g4v9_~IrJG(}HzQ&G32a)@}wuU%>6gTx5t2D(vrV?jVP&CH;m+J8I($y3{SM<SiOZ^XOMASq%O@KFJGV7Jq8{cD#M3w*Cb%~s;zz`yo-MY_0N03y1RFt`SZNmI?>LO!Qcq&f<&w6H$B;cm?DR?cfI^m<b<t990s^LPf`J~DL-SoQjJ2)d!)BDfO`_eYcIb-;BPKyc_?y4Zi}Nxz}`K#>6o>;!s&FMo!?P;e%%2$UO5VH}9<_9K`f1Cj@49@I|Ju<2in{XR(JvCzg?JP4;C>gTj7N_AkK;pP-*$RE5$PJEVZ&1cZjRHNRJbkA;oi6JDJ+x17(+x7du`8DqY*UnTws??9){2KZ(!3R6NYyZLzQK<uDV2uFsb=?t2%m@@7eBa(1v4g$i6yYdN6LUMk<zkJE+#49vFQz`MV6y8-ws-&v!qB~ewT9miL@k{f%;!L%iM@v<_l%x(=kLMOat0LPPr&p3Xo>>rc+{QSpQUp?<J<un$+n0$>anLa27esrPtU*fdsBBf%9MCb`Gge17o`XbuNQGoAI6_Rc}H9Tl{EvA;mr*43Sx4nG_nRQGqHo$scFq$XykKr=wF7oHmbE!EZE&(#QFiOGc0naz1yE(!q$#vus@>kS}0tz*ihdum;0edV(``U0;z^~$8mDfW2FPn9mazj1j5fxFh?1ZGRUFtN9cKC)VGt(dcuU?)z}L+TY^N!Q@PA~D_0VX8{23`iwAT055_5(7dM{p*%qJb<%0mUoG%kg_;&JjRhT)q#V5CZZqwgYWp3GKn&nm4Rkm4TU7b7u0BFTjH>kyuV_c$E3sPHL@|TN{cAXdnZ5t#<ICLjkF*E||SAt_ax8O}^rO1Go6r&A6&~Nj%tlOMz>GCc&vD&x3Vcc|lRp7a{5fNKAog|JS<f*3li(S;jeP(W2nNiTu3R;)Q`SnEeAs%k-Ny_P(Wjj%d^yH*4XVPu)nZAQgG0L;l$E>2xc7{f&4blL6;7?L8?VH+Uu%H`*a;udE#At095HsUbEE?p3@f!hcSKR&1jhAKf)N5rw(^*TfY+}ID7-TXcilME_N_8mJv7-VIn}bvgx*#?Hg?6;9j9~hlA*&qlC58_dCaQF{qh;&2>)r7MbQxK<j}}0TDbjDH*gDBOx94<{)v&X;#sssBD~{Wyt;(k8M6*umH08JVQFIIdSso3AD;-IDQoU%8NwwOxELPfOe-PpA4!wTKg}D|<01ZdP2DsLm={GX{Gi{LYG048O{ZN4yhM8#9G!DJg*0CrCr48nD8;$lOuiYKhw-XCXR>3PCO9A?xSWvRcab(~ZaJoO<)@(A`pn9<O!s6URxS$%ehe0rjwv`#h9vQy8ZHv!z$ntYoXv^3nx=tL6CHOh$9<W<UJSjeA%E6ZH4!rJb*q?*8g8P^56t<6Jabpo=11t(P!#M(rqi=?@hu{^=Vz;)+y3VSoB0k}_yUMTn)=Y<qZV=UUZwOwkw2Eh2HT@)5WLTaQPO7fM>pH2rrls<lg5FZ7m3qZV1<SgA=F4baS=l#7J|1(`E1M$Au$x{`m(2S>)R}IrLI#Byx94h^?!)M(U-Z#PTVj8Vg^b+mDu>OTgYI#fmNDf<q#!ZPIyY7wBKL}32ccvJqQ0r39~Y4T?S<>8hye<Zh^F#F_UNQUiitl?9&(iNFej?%S1EK~<)CX<GVpzsi!YiTudA!rC`I!{6k)Th%#bSY(PJ8OJx}lOYU0KQsFbKYQb2b#qk-p2IfA|6pjQ$1lI@LU@r#q@7YeQB%;gtn5q@#9_{Gur1>FrGMdKGd5^%G4#?g5OOKJ5G(lR`=LquO$lxG~BXA+cO%|O|%XyE)R7w2!AZ=B`%X5hyZZa}w$BX<A_XsvF30qKY1K0c#xV@S=WcR`UJiCx78b7zM+b|FU;a?C=xyhwnvZ$A*nQG+k=l)`@r>%onchTMwj*R@o-L*>)y^_S*o_a@hL{D$JhMOyYIcr6#Jma##zH1w+BWW14pQ0~#+6#{_YZ%XP;Mb_mhB3I6}sgCNrLx{hE&U9|9G|~Bv>U@&!Q2BIvJ$3P__XT#pL*4IC_rJjIcc}ZFr2EPB<1yWz5gmrYW!d2`u1(iv#l=)d+>5ALzRMiy7ZZ*}RSv=z6OKjI90c<viQ*R;5?@Fp@F0j<Ojnv}l_pxHNp>ZQ{?6Ues`OqRg=6C1r&{_{q?<is#;nrrsVBhIbd<B@5p&jUC@h(^e8RuLsj))OS^(yJR>+?>FH2@KZ;fBJq%=z;-|&<fTP(*x88`?nK*@m;sc{xt0RB%h=fxL%glJxT!AIyO<s?4|gI7=T13=K>e6i>fdjOM^6v(1W9MZWFX*W2IgiHEjLht$sO?0eK><|fgyPRuM#c!zi4KIFU7EgDf=U{Pc;~xE8AprOAuQ@BQ;G={!N(Prerji*taT;@pqvlRY$)Tc}J|!WKIB^=8#A&DrSacO}8e(>&iPKQiv*_NK#j}XhAmUIy{9PdcNSuaEoW?BTG%}Yq%f=>-FJW((nqE7sszts;z{jxNv!4&rn*XlmEvY4w)1P{nP`08q_~GA!TCcDc8tjG?3mTnLTjeL`ushoah3I3}L=uFsi^C(-*!=)F@R2>NZD9a3PWy>wpX<cqHsII8n*oIe>=@(QuR}jjR^Zs}w9!@+S$1ZlKqu(=9+mK~1N3m(opyrAD8lXJP=sy(+<uK$08Aigh4yfC3TOPA%8k5kIu~fxz5SapKuHQ>XCn8~6Q!Z>3TwK<OE)x%1h4T>z)bJDaT_+{=p+#IG?18%u9|oP34;`^9gcfOrf?t<2R7Zn?`el1yns5aLJEoVvQLdNVbBS<ajS41bZ);!Tld<59~*_H5k7uaIQFI{X~-Zv@+1DlX`v;5qDB8>CJwGtjSHhctk{GfB|Ud$hc5E^BhUX-$zf;M=C-6SrhXSGe*4w<VmhQFTzQ&ye*5!@-%I!a10=R7HX?QuJFw?P&_7muT4U!R7N0uosALw$0K~HNt~(wCF)x0^i=UTF_PBB<Z4rmG@Xeq7JA9hW3(*nd4EljE*6?^e02rUw*f)RrQ}(%2GRdt4+oU-IQq9HV_B}dGE*`isXpy%+V?V?bqJ+gKZ9fX|K&5%g&fH#zZQ(1Aw?EU%MDetP+zB5HSYaB)0SK}C8)m5iG|t-&=pi{g4zE=l9Tw7`-i;8ERSR<+GmKuUDSa>vgJ_k{Xke$t@b*`intXtAH*Fa$xbV$i{U=377=q$)5QqMol3AKZg{88b(lAO;@)8)WWT3CE#Uoey6XG012Zjg*4UTe71v2vH)Nyolp!}FKaubhXv0$-z`!z`Az$!+ke^3tZbWMkD$c|t*%_2P^0r5n4j}=e$j~nQ_7yv(5z<OA8Z#se5uxI8BylX<{I(9Gd$h7#(yJo26g<aPI!f#EIYeaNG9o-#(@B{YWJ3KMxA@LLrA&Ntv_!QlbLU#xaOgknO`9tZ%UcoDIs(7w^0MP!3-WEyU@kw}?6%&%3K=I<r=Or_<LlMY@FAq$t$JKNJ;^z@E8T|jq)nzaumAn&9h!GQFmyg{jqS*(mG)Zux;_V3Cv9RZu2SvO7?Jw*yS6+u8j$F|(ScqBixu+9_3gYwRYC<r{23~|%*t6nt(#Eq<RBrg30DcjxXU`}_r_VSW{^hU#;=iIXmn7+-I+E4P_Wij18qe0C@Gt(Bec#7j9&3SsObb#dK7h4+<W8vgPyY)$6&8I1B6%Sbjz342<lA4k5v%X%MXvl1XU8}H;b%a<;lNE~@3hyB{dkDEyKZ>lqI5_X=@R{gLmd!S7m1ipqNzp4B3*P2If%_{TBzt$gdK!tmYaCA(9H>U;A-pTNQm1rFN`L10BPpx467?PC8Jb74Dj+~;Q&8rw(yn9EG4y#bNnpm@2y7NkmjCT`+ob6-+c9Bql7pRLmuqAIFxIwA^nuNI#vAbPu<eCv5HZHZFIWhZIUZJEH??u22+rNa(sXR{+u06CoY~C@Ee(l!vJ2xlq<N+b?Cb94n0!b4o_P9=Lh@exBvcR_Yeh}=1sY`-`d}8HTF)el@hAbEfS<4`W{5&9q=)0(ZLww%Y#v;ms}9FltmkHRSm1Ov93BS*PO-V>Ie!qUfH-r*_YIO-S#FC5x=E5ll}I;w}1P0cA*Z@x*K#tpVN)=9G3liyX*zY9NsX$jf2I$){BuZK|xWzL2GilOLUeFigy<Tlefx<h^SxVap>*OQBBl=(qz-zS=GEV3JpU!9PIe^SK|s-Tq3<pOv@)9q^5iOD-?<P!U;w22$j^;*yZ|!D7VHw^@f#nPw1o!*(h;0ks7><T%p4bE^#%G5-X*`LJ2%ai@1A{*8>^coL+b#C=f<3t}e&}$%}B+!r)Q?+mGUkUWCpj3%5TGJs15hQ2-n4C|)a`yuP5ux<O37HKMN{gUE?}iyd*bvR*_koHC@OH@@^?Ay^YmL!bo}v?r9?c)}?>rkc`Ys(6NiCt#B`S`_?|uc;DLNvd9riHFW)Qu{J=BP=MiE>TRVxcZo4A-=q1tt_Axd7#GtsaF`S;tn<y;Lr2hUtUaI5>_U({**RUyXY@8Cgl?&5XIOl=;I1|>UQw);~+|^je)>zoftvnccFu>(J|&}9Z>FN5&1Zckme(_r=nUu=DuclqZ{cMahIn)jvD%<jaYvg2}xnQA1hQM3R8yDkPn;fZ^qDXoa7R3c<2$vz#m<%WBG6Jhd_l~v(y~OXpWBoA8ij+$$wj`GCEv#05~55#Fcuy!o9FB1SPSNUY<L<ckSZV$VKn9kdGO9(*k~-P|RU;SA=2wD2<gEOECqyawJ8kwn@WD1T?JX5pBX?kYR*eEDu{V<Y=ITa2#hbF_@<z(+AzElCgym4}a4hrrdZ1yCP^VnR|&XfECxj`O!}{ahORij7aBmkx)->LfFe%yFm{&kV*&J=kt?T#1+a|z)nH)ZW01URU}G%)KAzVWR?2yL8?p?4~;U-)=?s1$i0l)BW{1vIy^qLv(Q%!``y|<x&5=-|0R`=esMU(&Ts#`b-0^k3tx~oUKq&jzOE{fVT_%yA{YIj`5LoOuRZAG)uq7@?j<;~pQZo^Q$o8xifvu(^KJHJ-+ha4q%q*j&fDMoT7waQIwWjU{u`3hC&6Wa!$W+kaT>^eK;R>*DmMa=L8zzfM!>F;RbZ(Ha40jPDeiazag#zgVtC^mE7`e3Dbq+M95S-)V@-^6g^Dt4x@OtOxB_%1^B7D8STvFB%r2O19=r6ijAL4AVj61<hgpU(G$GBii_J8OY5v?Z%wqI4&nku(_ZBjXapxHFuFf!uVP9rg!)BSnv|g~{r==N|us^|1jsl}d-Ps1PbNnpRqg(UsUq|qflwHvH)r16GS$XIc3>~_t*^5Wme8wHhiwB@~&oz2AW5CW0d-+zcXP$d`!^rlPYx8;rA6%>N#*5j!a&81=o4YXbW3)>1lXgbZ>M+~jh4e#v*Iwv@(wcAYA_}9qiwchO&0QoYU`P-hMo+-ZGj?Uw$T4-D1iVzSiT05kJJ&gWGJ=}6a_yCQbMtLn6ojz6mj#HMy3oGGv1xQcONq)DdN0Z|b?qIVu<z3ks+3{nI(PlZ>nZaV3}m)(>xsBnf)pFZumWOwj!kQ(NsGVOmv7X1f)fP;A<ZyoJpn!;Q&twonYJt%GtNj@E7O|AI|EdB?seE%(0#30B}`+MX3doCvS*l=YsxyN9}FKT&o^W}p{o^Vm^Q<L#l;{9^fGQW(4h4$_A7O(KF56Z+}HR;w_Y6uZjX#t(6emYl^4<_QRe2EuHrkGuDBl5;@6z!n6A8R(-kWUZDWSf3N6U6&Ma%N;?I=KGFNfJl=q~&!72G}zb|W*v&U$ODPs@W5f*?UIuj4UQ{<nSR;vAz-F=wb;<l|YQ0?!{uuttBCmyrN4u=?pL0GD0n5d)!?#IZ;EK7UKuusYL>zr;9Vp}|%$V|(Wmv5NjymZR%d*s`sxGhRHo^O-Vf-2>iq@c5_nuqbnT7-*~MM|4OR5-&Ng_qd5N}*t;>`|xFI2n;Vdz2{DoOqf#m@-0XN-~bS9;qR1hvIr#O8#h8sOI$I0{5~Ya4{uqgF>?t<8I_=ih_-O+6aY_50v|Qz7dM=BtiamU&H2yyAX7Z<s!rWB%W!S@Jg9xr{t0xigs2!hdtd5qr1R>Pma+^s6MCT;Z3f^iK{w%#S#TGtxoCH0BugFSK{v7DMMTAdp?FI=eoyJcY5Jv8k`Q`gEgmkUAjokQjb>HE;n_Mk2^q`Wp*06C<H|J$mE2YHCK=mn-fxt?!HBCAB`{*2BqVHXIw3e0&!n|j91do;N;CWGDQFhNQJP-poA?^%zb`i27ZZ_MAQbo#ax?Gty&)W<7upnK12yIC*rGsZIt=N?nom$jJ0UAtUSxefb)vRV!e#21fu}XKmiz%eB+U@|5@b0aoT2Bgb9NY?<w8Yq*!jKO{H+a=5b84mgicIK=Sqd3tT@m0U+j&v>cJ1#b{<PWHf5RFPtWcnTYE>v#mw*ZAJN(qSLe1;c??A$5iyZaee|TUaq0&u!UhLW*Lff#Y7o<OgE8~fhe<%y23usGGwSinq`PALd?=%GVDT6y|E`Q_;N`O9I1F{j#)_K1fIhvN7{nEBOlA+epJn)!@d3UcJpk17awDPL504Ac1YFdyL=uetmlD9=5|~D*xokV#GrVw2g+M*l}*PqAiw!_VU^$F&2Wz?{`T*o-}-fMu9i`{v{R|p^>}Ks=}pmeEvxO%Nx9>#3qxQpuuc$o<3bSfw=yUr)p`>B&2HPNX1D#7-L`8SOYoNU)k8M#WHdhtdeb3ZH&jHgY{<UzXoQ3S2Dw)_P~i!89{Re6v_A>L5uWm5oEnLNNIRwmL{^&iLNQGber;VLQa2FUn9T$7EEWd)?=)<b1}r(@?=tZ*0u)J9oQmYcnv;V{LXsm;8OX88gUt!@Vn^XXzj>TOOvT2{*41mq^axxsBI~Ms`l^P+QSGBKhvCTzI()|A)Dzfnrz$)s<<WPFgSLB5A=Hq;adzp^IgyznN^%3(!mB3n0#YoA7agOLj}f8OO^~8EE7~1Aj#@VhvD71q32N01h1&YYQmCD~+(YKTr#1JSLdyJqKW_Ie6vZoK0zXk8g<|SyKMlo%dXA1_Z7zy`GW9x~#X$KRyNr8dbla~J6fp?lE^k+nkn+=9XTBAFQIi;!`KSsMx3UNL+K`3OFzAY-CD?=mRI=`28Eqo!A##%J4AEeq<t&TVS2NLasNJvf&{ElHa%s2mGsd!3sa7+`GLaA}VB?zbOE^Nc2QB0r6|yaj=<+<-M`ZaliLP(jctYrnBT`8<jLP_utRhl<9!k3c3O~&RMGCgg`0WRuDcJ?vy&rtWcD3fx_<+Ve0i__O`^JjxbLg}&Z*c+k9rr_Fhd#UgWx3~-_lI8JC07(7!7y)MG+RC((ZQR|5Mz0l<`vOu31`*kkE1Z$WcZDcEk_OK40}%+Nh^kBhCtiMTb56L^A8F)vDqJMYDr6<g}RZ32_t+<&BILn$bPIyE!1kA-ZC)DBH5mQ`!`TOM2&&s9+3A#qA~C^zE9l~P30<VsV9=MnSX2EIPyuzn?ut#Iw~qPN~MymJu$N6A!WVyld)EA&DE-eqbPZ2iaD^S5F$H2qgR1)k+7afNs!o5s^z?qQfiDVy<;T?;uwMSn0Xka$*`_8sd*TnL<Z%+@44t?l844@LJX#zES6nQ6uR}f3SGjpI3DN=tZVqsrX9tpIU2r(3qJ<T)V4R~B9eH_XJR4G6ldYUPjQwai8GHRl3R6r_(95ogpo+4ctw(CK0*es%tDAB@0y9tmDe$1yCh=HSs0!DXhORUnm*(rt>c1+OD);LY-EzdE;@N?)6I8@QC;m()7!-9SmJW>n}1^5^*ZslHqfz7uwaRwj^pLf%HXGD&$PM34C9C{g5~XBCMafXsDFPJs|20jo280S`rR&6gu?G|nbO<;oh?#?#QY^{^G-{Ylea`Ur5TvK-v!FaUZ8R@SZI0LyzBDh%vhf0qV)b3Cns-l%EjeFElp1D(v*wJhg+DOxeL?6NX=Z9w%%b`a%L|}gdpJe^5F-%9KBItjmZR00_Y^F8N0E!%9{RYI@D6w$Ly1FFIYSGU>ZOQ1vU6E*QD`c`EHCcE{ac1Ph0J?#%D*TjXew=q5rO6IbXz1^sZyPfIcgqZL=@wmN}2fO>I<$7+%f0#_sz7VdRdd?(hf_r+BXW81}qqclO_Sm}b<Xd;3Y?Oix|x9tAyb+r$Ku<a@B)*ZAO!_<~vxG$am35bXAhCKaLpKu^bToEGLk{Gm}oJ_L!cdwSa{i+*y%h}{V@@eNSxxuFbmDo!}J*=gsM*NrP~6!{nGy~-p82VM)3XF-0K&h;Ji4un4iE9~4he|x|RI+sd?`PF^{sT)S>IC%4B$O9YV3Y&z<#1Om5!ovlZ8AMZR2vpNa#eEZ`kw>~f$S-*S1wleQHjVx9ne_Fg7mF)?#9uC!)kP`k5?n&&&B+t-7DW5s%_}DIVW`a(4Myv`!y%d!lXk5+VHW^+FJ6kCp%d?%ZebA}c2+uplw5-;2ha~XrFE6(vP=F{ys<+(0K`*I&}osay6sxqG0LHfUCZsLEd$6)kUa7S`yrRu{H*YD@~Q7#q39(SIVhS$X_0AIgC8B!SK$!H>nn#hpj0HHjYfmu>Ogq8k>Q+D(W|W=62EI@$$fHn8lRzyQPoUqT>I##@<t(rIK3epZg}hDgY|iUK8>}?{naE5!~eOHh=Mq3i20*4;COOhOc3LN{3tZ8nlnJz_yCbTj<i%iqQJsPWdxx??o6W_?t5e;qrb%{(qz;bB`E&j`8a8ExK8DNui4()KWKb%gr&|K$4$Y67)ErPUQ=I{(X#OQ_oub2M8`;^JJshNci~Uc2SJpPIt0E_F%>bOa1sfH_g4>k!XL`jVwb#lDJ2G;IMH&LaDC`$N$TiY1$K<XBJ35+AdNl0i!quoK*$SPO-O3LL_%R&#Ty$hqqxH<t~Xfg1;BbqujpXZ+CB(4d=Mwe0eK-H@ZSItTYsnrgTVt09LypCE~!W?cp?>hBbq8lScX<aB%!L(Yl-|MNSf-X0?Suty}uER9z6@yjM4v>O29fqz;O-2<%eoLOcUwobhmM|-?Zt(*LJ?Ti$!V@262GS*_DAConC>=#&_1@n+o7HEF!p7fk~+(X+f0ZiQ3~Q78Q`(N%KhzsuZ!3Lh2RyEW!zVVPGOct5oTe%v6E3i?6k~+H3#%%NK6>%}e}KEk9_#y!Wr)u2t|J7Zk(z+LiyGy!UHvBS{j+-t{S3*t;FH2tWY%M-(}n35wLeT@A$`Iit~Vd7K8&09pdNvE2X(XjYD&&k=sKAMEg5I4;7D@PnT&e757~bJ!7n*nQs*v7g}g5uAUjs;jE20Z^LRJBK%RM09snR#jG3R#sM4CI~RCXwGa}^g|E@dR#j#f>JPrnlYOV6l`Rma7?QYtBxxDhgL<CDAW_2NZLL8J4fNa5e?=t*g0wu$L!*l`?9~4YGdPTA0vnB$*lPsfx^COg1%zahnI~98(;t3-~9Bk>i^;LcUQmr-POZE&8z(GcYpKiik?o`Z@hz<T&?IYWn`prFzv!FAP#R~e>HeIpHwS<hvDZXVK%(V-&Fh>H+YZ#)I90sr)J*AeP`%-3T`J-2Vp8Wbn-0ngdN|H+C&3Jg&OqS2<Kt9Di~M~uy|j97lS?0jAl1PiHaX30Ken0fTlhTy2E^c@pa9MaI_Q>{vr4T0R(A96E35T))g_OtU-`juhz(&%>7X^NJ$fP3`OO3R1IU?Q%MrZVrr(bK06_0c7j^Jl0#wa7xALw(IAwHGmAjLAEp@ye_4r+-BQqVnaRYrN_xdTMNudqAN<7aJf9{hfHhDt0&!BUV9b#^>NoX~KvAjb!Ut%JSFpOU*}wLst_mx4825l)vf8uo_cL_pJn)XOWSrbq{l+vA;&*e0k}1@Y&8r(5BeT#s{)ufKLkGNz<OM9Q)t|(DnOTH7pa|5SK{I(nlQ)*%AnNOsabM$g3U^ySf><c+1uhgi^8~PiU0mRH<}mK5!SwZ@V&wK3%%;NxJvXsYutE9uC1%utDl#ufLtv%>j2*gm?t6523NsrwZzCZv(bo}mUB)O})o6c-k(>bmyO%~WT^T?J(G+mrrV)q^U}5$pl{65!R2s%UGU^(U$_k6BY~gtUwrVc1z@b4#B11A_<rwyJnB1E-cyz8iK=&njen=mQf-rEE+++6yI$qfmZ^#`KNuf4#Xu1y3G{(eeG#ZusnkPegmBUUNAv)+F-B0FwxEyT(&%R-pWe$&iGU{n=n|jeQP_MGJ{l|atFm}*6=XXI!e#arvDP=~E^DqDO_vqvXd-fj?5+8r?x-&F6Y2V(;Z*S$dCgy*^fL%U*q9@ZMv+|$*hyUt-5jQ@yXgxd4-5-ANs(<>&cDvF3(?2}I%XxbOn7_$;P@<>_n#ad8mJe8DaPiP}2chY~#1W%^NpB{+B3%g$Q|f}cZgm@s-iMfYvzK%!AyWfWB~8N%Alw`JR#ji{K3&Z_foZ`zyT<v8*Ke*bo_>Gf=RtB~_{>kYLv)3yR%0@Ph?*KPXm^OB>ihO$hu6kqn&j}k!B0;|A=Yh3AOQ!uAOC7}M@fcCMJ4N|(PUc7ri)Qnqj_9IZ4#h@8hdirE-}(yJ!<X7SG8Y>oojuNM!njv$V0W>3E~*I%P)(VoCdeDiHQ4%g#ai5X(W=c0z?C!s(vk3c;&zdFj8H`Z@qIu$!$bR8TB3FK_sY&$>N0n%8K^H-x>&@Xn;pcd$Jac!T|e(`5v{8T(hf`(E7F!!46{nx?dHLKDK+-w_sg>8{&sBW%#DbqZkK-ce*$y`X}ijsNj`Lx^8q;yCnT>ND~^KU@`=-+;zgyRmCsrA>k-z8Ery<ewN~lxU3LXoUs~Oe9ZAyu8KObBo(SgqXuXvhk!8Z%%))#QTt}}&HEDEcLa*Hb~$p;Wf2;6`Cy{`gn<uXKZXt5qkosNfc*8*4twp;i>9KwkXM>-U#j)RrNS1QXwPci;+5!WtahpaFmyKj;!tw=0}YJST5&FB`mp6NHGMnjac)Mfls1EvV$9P7g9T&DH^f_>5IK9BL<6RIvN#Q<!)nrbSEKU;b5#aOMe)QZ6e*RI=1QZY$<6Kzr7)B(4@plr#8k7Qfg@oE18YcXSF3CTN`_H2@b4vIyNs@`9J)AsFEU0}>|+g062ELmy}H+OcQ)^VvLK*L1(g)|()>=zh7(#aE57yZKv@u0QYZglw~+AM@SIjAlpZMb=W#H}hKa7a<~tiu>0&%wc@B%$EDhB}BQc|w_HA6fFq|BXk~pmLykh&BYnPLZ$I*1nN_h11EzNJvU!OEsO^*7DstJrVwE&E^_(ndju%QfQEW-?B`uw(`RaD~bre8osZoO4io<A!)oJ#WMsj%X+39SDi(&Nc&IwkGdShCzhX3`Yfj~FCiwS(C|g-O)hIoh38!)6rGc9Ean`&E4}>ABUlFokxF5z1r~ce_lMv0Gqu+2jtrh_DVH6wJ#7A|{inSu{8D8k@t?Va^tD7X^NrjIw8GGNv=msxphx-MI5^2+bvHuq@RbhIj!5cfE(OP%S=$OQ?rOr7r5(W8<P;DZ_j+^|bN$cS*fp;ADHJp<f7m6L#=usO`NxJ@TG_rVl&t>W{aSvZ;YqmLFknET6kW=vIhM5;stWzD%Im--KBPJNF;`U!cLbRCK6WbnEw=brB-qzW5w4)$r<aszyrZJhXE|Pq=pm?}_!0yT_`RQVJ?cPf)dSA&oec(m}^TZyOp>7^!SZjuQ{23MiSrh}22&Vr}O4yVYxV&ems?A!`yWMoG~7EV_{`Pg}=6kB0dkrKE&vbHR|E_dico@mCswLaWQm-lhG@&>5zwxxGk6VFO+!X|;m<pU-ukP@djcg4;u%n>6(uN^cpPxTKfHDEi#=Ipr$;PG(c{6W3_XWYDQ4aGpz5)0{M0Yo5lCjjjTdo{m-=(v~b5_OV3GYwb22s~G3s#7bYr@5q`-*1`3qil&B36MzfkzTgqqJK=>O*thl0(Qu<CSH2+Wb4yuao(%GH#1d4w?MnU-_9P!c<+0#*Xvwcu>UA=?cLu=7(7Z~;7gij@_(T;un#h70$F$z6c?0pcLw|JyR37F<kRDDkfiw~3SCyhwVi?ZZmIUBzfoa(d68Uk$xt`5<(>#ewX)l&$;mdf6pqI@n*wgY4;D8+?6VAW}Zb{%)5x8Rmw<U1f2L8w!Z>zOm9e6v-8=IS{F!|t$#tPte&D-)<HdX*{)u0J>WA7P_w#Q|xMum>Lst?maC;0kz)!$_gs=w=P`0%&p`u#An#%;W$?_(x-v%JG&rgF2qm*dM#8{(s5Sx6~I6N>$T`qfdt?nl{4a8gZu?O~ulbo?Ugj%H&@=G1PrF^wZe|7bQIwYD+c<A5HTkJ|XqDF}Zo`jyw(+;(`Rl`IPR>6bMrKUykM++!&&S0EV0<6s)d_EU<tY{0{dANFl=C*Jd%<!!Gvadjc(2~4y>rV&xKsb1*qx5!{;@W~H&0c$Q@@kuvrn4cQ>lfSFBO7se&f}=j6JI^&O8Wq#rf?#C3!+|#sHvMIXq_UiE+R!6?VIgxy$&#Z>PO}g-1RIY}nkT20{g0X@Tpi6S_wN<tlEP)UMFK&s55$S()hK9}28JJ{e_^g>>2D7VLzP{Lg0j3ZjjuHwq3>#j>EegbF0Vz$d$n)18)o`O3Nl!Q*K3L4XjrUBb5#_z=mkn?&O2m_<YL>roZ@AB>l{OY#7mB(d4^*!Owozwpr&f(t7Y43wZVQ8_MV3c`jjsU--?@WN&|fqfVvr6B>dTO$=KJ^gcW6ib+~WJg+f*^G2g{e{|$NBDRwG+@xCMn#r&9G7BIyiyH_|p0*aWWdjUy4cPShH8r}wX>8|hWl;GC__<otY$O=h%XWtP^Y?t_tSZ*=0+L~uF)mp4WTa+xyFb3gl1maYTR!Sx(+dym>qjE6Qa;t^-!;`5yHHYWxH6!Y&)=Uh$tyeVf7EJ7)CLflX+}54^t_fahUz0w}7kIE;ox&#B4&Q|SY@aZ&Lf#srTw9jkMUpQOmg{jK>3)*`^o{kDy_|)C^T{k*SX7nBY-U}PT~{!yy+n;!CpD^3Bc}n>SnEmN7ciOhD4qkwF)VSPV<Z$_9lX;HdcCKZ&gB(4CB-4ImS`Xdn%t5R-k8fpc!Qi0-ZXlocNbN1`Dy>2ZmRehtygxtOHEko6<^)$PwKesJStAo)5Q~L6&i;fwj!*?G9$az(bZ<jBwlUaE844dtDWb@S1oi~+nVa8E@|RQ5r3s7ZdUQMqbpUKA49Ie|5fdqs|fI^-O+u%#CTV=S#ZBF!kR>rmPApm=I!Qtf7j>DX4ALi#V>Fe^QeKrp(&6s1*Q&D%)?4ocxn_`uI6cB-)kZkI6iCFB00YAZ()P?3p6qplH~e^w?oKNscN|zD+M9R@=G6{7pG(Wk;2yIk5O-~KXORy{P~9NqweJ?cR|8@x2H|;dCgnYybm=mhF>xKjNv!baU2echL;G1!*m#B4aU2%k#i)yhNknuqCo3g-=Q!3J+I9Mfw~z)G@@X_iIlU+N3ByAX{2{6sCk{5*VVf~*nwP(T>`jpy&)oMG-^R_;J**>-@FaK;lB^<0&b+e=)JpuV-}jLC}=hu6j#P!st$opL!eVHO24On-@<b+>QjI~7^oR+!Z8f_EHm9?&{EfKG`$BNpui;0P#&$P3;zAqxB$}yV1gRXCCm^LvuoJlmG)%bp2@m}#Mm7)z5#|UYC>0Y&*{L<=Yp(v+t|2z2WrgIJ0mjPT|spfc5(!D`V!q?!upo&21cP7$*)->PhI_1*HM%|(0ld=dXMSe;g9YBqz(b*vSZyOt8xvO@2?7(wPB|u;Ib%Q0@tIP4Kx%Fuuz?b0)Nj<(=Fi&I$0G;_-L;T>$|2kSFG4)0ajg27eve9+y|WLoF5iGrW)^s)BQrZOq3H%A>h0<gve2rG&w9u4cf+)ju3r?XAt5AegBe2*;j*&Z_BL2hG|uC5tXdr1v$qFQZT_C^<fO#n^|@gOsd^vRP)l8@#!@CUjBfIlD?izVd8xkjBpo%ae%*_n9~Gz&7z!ieAB;vpo4NQ=zWc0^E?W`*3_Y*_+^i_Xt4OdjHjDz-l4?C6objL6w2kM7F&L4iqUcCF5bMphRN^%ugyI4aup04a~Yw#7!U>Z$?vM7gYZ_-hJG_)n)H8^`Y>}9%W`{dL_kldQJ)b$Q(3+h{O>PA{_&0-euv$SKuolJ?{7Ur*|Y~$WS(#EdQg?bsO8;JKi`?tv%JhZ_{lG|B9610<rq{0R@Ex2ay9g0$>xja14d*Vh3C_7f^q7_oFH)xqtWEWC<_M}VZIGg!yQ3MoDVG!1Rt6{3<rx@UBwsTu36+`L~Jm8+FAoB8{h;K&2daH7n2|o_rxep3xYL(x`sqYM|4AU=ez%=&HHj0>`JP_Z$Vk?27TZk8S{OPtF<n!)(TwuZtVkzqys1d()fcRkNTr%Vo((!_q_Y?=M$)E&OV)>Gy$QmlF3IDtRW$hnSlmnGfo1wBw)1OJhRF**Qg*Wv}E~|IwglYG(o)yJ7T?2i;Y@eo+SA1MKS@^EE$EQ8S_t!-D52{lz&Ipmo{tSH}GF;S3}|b0mj{!F5{?oma9(C1kCjaZ7?SuC8c=*ijM}0BD#)^Ht_}XqhXTv1Tdl31i4hW9*S1`@Uhu=)Yef9Q&acb)q2B~OFGo_mep1KEY$$Bt61tBm<`ofgS%0qV;xymthG=aJi2r|0bnY6f@0*0n~RS3zJ|~c9!Ykl%MU1s5+sVxbRm*z4#z?nPo@-i2QS^#@aYLzS@2<+Oteq%BtMxLrnC47wUVG_F{TG%C|j+~xXT%IS<(=mT-t5$%II~5y;enR&DGR|UqQEfrqcULn|tJ(&K)W4XpqZD9RL(_L{rnov?lrao)%t%Vo6}u3dF`KIU>A6<#lPrL$*d?G{G1OxS5Y)6ns_>Ixl0jB@&F@o7>&&5|H>ze`wO6hW;`x&;<4>1m7VD{8w#wbZC^50`@CXgItO{AyRuHLS^oXVCwn>Wt>prGEJ)YOFZvFy8Dv)Q@tJeEqC!%P1_-RP+%+yDz1@VI9$wMNV;s`lz%`&H(KCZeq8Jqiag1SP=&G(zLzfw#cru4tnUF&w>nkxfM!|EyItg;Y2Iy!&j?$@^@M<*=(wI}xbn{m*As;+H^uSn<(<7+!=a(n94Y@<(?y@Gran+S*$ZW#Q1vUy3fWLzF)cY<*im+Ay^f-GBnO=G^=faPQ?IuWq$=!e<3$cEXi30WP;V89u@#h*rlF?YB@%lpsNpXB@iW9EDL|Q2fLsDnDH?)PE;A+NNi`8avl8{hDn-BF=@{I_1b0v|9&P>S9ZJ2+m!a}vG;myshC%<iexY~#6W^|(gVBK`T5vay(Y%Y^O;s3TjO0_p+rQl*ZtF8E1Pn9)b#2?!s_PKAfu{0ofTti&peG~Z24$An<KG+zN-v35l#lu)<tMW6#8nbq=Nd-l4r3=2VD_Z!*(iwLlhGl=U~JofY*)-ofhNepBaTvpE03g5`&hgz5J*R?@4^MKFbsXcdZ#qFNuw-SKB8h5JHLo9Zy@8RWv{IQk=?n~gvD2Z$}}1nv>}hAC`svF2Hg>)0lChPYcU#FMYW@yhdvYZR%B?k1r;b^Y8B0yt;VMB1FV8+7h&3swy#8~*rvS-Z(t9j>2%_~=z;!)E*@$W%Y~7^!op9t(<n4TE^6fW3ntHezjt5}%i8)WwFDj8KrOU@EvOG_pf^0U1Xa=U%bFICTwcKFhi>|}`k@VR;UL<;(YXU9tj*-7kj1FGS|p86GvX7v_3@r<ca&8*%#t`P8mb1xH8u8tpay?0>@UL3_`$aU-WCDMEps27#sRIJu(vk1ERzh&Q_`%9+Xy{J2BYvS=v6<^$;$v_<g`1yX8Q+86q31}a2jBSC4}INTX?El)912Z*p;2?yA!CGcV(yg1_j@m<+2owL285w9U$vJ66o0|337w2y}2Xf|1vN|&v#7EcSz4E{54rCox_@lS2ogaV~%D&R-aB`F5#<%c!mAaj>HzlLe%pOqY&aL_;VnSuwg1cejvUOFBgXI3+%%<?=Kw#aRN5ZCy3efcvlwAG4rU%{^tGK6U&8gUP2uz5qUPv2qB|0s5Uo`TO4}_evF(Zc6-F4rm^DH0At;2*+4A?1l$8NvW|)}8^TP;-Ul5W9)#5LNzuAObE<r5URh=B33NA>5eh1r0;=zzW$~0cf>!dWEu`PY5~>7%0^>@ixO^95!}G^UA)ecGA>iMd@NY}tXBz(274oIR-^9lPyoO(gf2-hi8^LQ~?POMik{8z$_+}12W)s6QK^vPX9fW=`Z5F(Xna*9G@H_*{;l~*s-4TXa!GsXM3S-F+!^I?-YDeAQVK9R~{J~T9Z93kcdk+t&*giHO|4lW@$9qO=_-LFg22In@@PSo_O*9BFhA-)GZp*YfC<JWxSJpl<LZS*-=hotSc6NB&K7RV#Wk`tVe8MnoD~>@^t73;M%f)~WhpYpBiB=N`EQz2NLln6Mf+LWFc3fd1t?}`M@e*go)&3_<z-3cQw?a!hbu7%#ak;_zodPMdSWBsVPO36p42<*Gu@sUxqdc;>Egna(gkq2}&TKCvw+MHd>CzYwDE;|T?gjdz1olusV>AG7V~j!~_mw4}Z^f?q7Pr+oCKXcTHY<(}X$d*(<!yFVE+Vt&ml`2-`4G&T8Qh!Y?5ll_&F}d5p>%}KqOobPjABZ9i-`fn`H!xeod^98i|C6AM#<MT+D6)!7DC>&J+4s>LA(HkS`_B7H1}n}M3~cew)S)0nW7FRmUM$ByZ|VF&?KJuaL{4)8ZCrv6;tA3UuGlF0#az}kFwQ2>U&zkE?Rt%@cE?SU6_JENEdXP664Jh_fdVW79U6H@)P-$$L$4OAYKJ`Cr0DLc^0bEAZ}MlL94NHr%iTswrj}FIm2=h^8g)st{*9S>YUg*=tnLqp3ocb%g*SnDn9<q6RqsL-f<58&Utojipv$n;`}JxC{{R7Tmz5GW1ys%s<NcjA6<T!&Uqq)QBw&T`Xy$WI6pChU@So*q_xD9KPq&c8u^#{xoDvDJW?14fklbX3jzxS5CWf>W~7}QJ=SK~oiNpqv|nN2+!7=#Y&C_pCS_OAdX*x;>lt5JLzK$2qm&t~4b-OG!3e+`=}AJgM7b#{E+l2b2&PrzV{T94+&pOelK@t>9&e9NeDHW>H@9Gs+9oM|j1@s!iQJg}5fdEnS*iCS!BxDU!jhdHac8~ySBkRAs}7CdJjoB_rB{0WB$>+BN>!wL<n;E4N1;G0jZ8U-YnZ{sGHwln40Glj0JkK#Kqxw4mYy)iRNXzgot2NnSNf=J5Ki-WHxr3wibzG4n@_@<ayvzXHA|mHi4C1aY~I<l`NT?zM7F^knNhduQQo_sqXor8M1@A=obW6RFgzC@9P2D1KJf9f$t2<v`^cF%**R16CKu;=5&pJs#hadU0wF_IY?1QPHf(3oV{)Q1sNHih%W4X*al6KXCJ{!{7F1%odRqzrTJo^s+eE_?uyC?g4XkG0sgfrm@Y=*MRth=;)4GWaACv*qYVC%>sw#Df?n$JJ4XrqX=)yy5WG=Y)BZ>0q41SNi*JoaqjG~^$S#0r${QbS0SZQdhbRF)srF{v3Z+lU2$5z0)HirVH#K=wFQsm+!m1JQ=k;QCyG9ctWQ6*qxPoY(24!g^Ej`j=nSYl40?+X)r;RYX>MusV9($huJx*%6_GScDcQ<kgn^oL_(?s?Vv6cq94+$Rbi9leo@zw=laTKf>%P-Bw`bQPbpQ*S)sGkxAv*Xd+a^y{jYbD4E^t0BXa!!?mfel9`w@spY4-Krtak8`>2HQ8?QqwJ8>1gCRf=kcgl;`J;@q3BRk;=v$?(C$7NQ$9+%(rIbaVynsXR1FsIFSNF3ZU>enpQV9aGOt^Al(4MuYY7LXHco#DLE>;gEig)2WM(DKADEu0_Iq|vT}4Tcy7#$NEGPM2V;XhIog<ZVC|x#(y5u*K^1P`@0+iZgz6;YSolsz2J(i4trtQF5g*qbiP3UTTWxeP9;P95#)?AR+;;x2fY+d4-ttJ<2zBD}Aen-dtmC}tqmNx?#yUsffyCJj?knJxOy$UJug*uXfk$Kz%{bPWr83ywV#KL5FhyKvsRBMvfBSUy-d(Ga05)e?(+Uac=#`$od1xo6{d)_&!7d4E-CPoLtP<vK_Lw$FeO@jE0H&X}tj#T0|jAYcUQ@Sy(8L9HXeG+h<>1TdBTc!l5d5fjre_07L7glp<wmIE%kVO&1^nN$*e0x6u(mfBCh6VhE&I!ZCM{P48bxke3WuBc7bAmEU(N%tJOuq6qb&p6Ppka8)AyP2`?VtAxK)4+?MzsJ1HNPlWQuF<UbVQb|x09Fp_IVvtDtAiT($xX$aKPoe22n~K;s|cT&Y_f+T&KkJiiMgA(n`(0XsITW>4uz7#b8*LR?m7-N_3bnRm$1!Xvr!Z><@`eu(6o5lN_QEk6x|nI013b`KRnUyYkCktV6@qsHih{BBj}iPKo4P8;gUQR&#Q4@?0|Mncpo~Mg@RUWWe7<2Zw3#^Y9cbp4tw1sqnE9?m9)#PC*3WI#QHDJNrc_hY+&Be%_hRE&HsgE>V=vb?40&UH8hvf=X=W3*<rd#!Sbm{Va}Ko~U^>m}dDBum#4>2S_8nc)5yl0*r|#A3lk>*TA%ly$xn{U4H&~8SJjTTZ*IDuX{!&h-9Qk>V6hY>lYXs>$lMq!#bQ|6f4l9^2iRqi3Z-2Aj9d{_D-W1D%-AK(9tDdA%PcLb-GhShL7jLY!Lbdw_>OWs^AjnTx@xunl8nk?l1h|A`HpeIcQArmvIJyeLT>eZ4K|>nzw5mcL2~Cbo5x=V^Kx5+8cPPT=1&nEb+z{GX*A4QrtsQs?wI>3cQO?;)q!`M4bkZ=LvW9OV~yf5-(A-U?Z)>L@^b=F#C>r6Hv#p|Gn<KD{;JL6w>>epY*}-sIY!|<5kFOw^IDB2^DOyAWRXCA~EBQCI-|zaR^2`0nwwatMBGvh7+W)nt2tnu2!s+hfY6vB7)^rtxaab-*gR^`RQaN&+E=3^yH)|cbbfXR3?`!IC1Y3Pwe8~hNeXyedUO846yg-(}3b$)phq1D*Mng4|d)^rMpa`#D=H=eS!22k~td1#$jACndMbN{cuify3+3HFe*53!|OBcrE%wwTSFHQ52%ICdxuFMUGL4dZP@n^nL5jy5nyN<lVPO1Y^;NMZoUYq(kCBnE?}BdusaNdpFv8L`W(qaEp(hxXNxEn%(<e0$s^kQ$SW@lVjRzZ6hlz$d_fd=!vNfBY@1Fk(1~YJN|6+~mzT{e>-(!f|14;s<<-egGmbFHn{;mlhMQ3ODZXiX8)C5c4G$(YouTV>B%=im-uDFtkzd|Azr4)k(oo<a%^YAf*fI*Jnngex7(m?C>wA9gb##?)V^yP^g~$rvE+pD3SVR{j`sI}Fd)$rCt=-*y`wM6>=$OguUH7VTc<O2(ZI9plmexUz+`6ZwJKji)8+c>uVP1sX@<kK&-Q?34)$*Syqg}Ct^sFf-oI??kZlejA3-VT#gd=g^X~EkpAi7#xwv&HW>Q<e@yjgiw;LXo;SAcFz2xn^YEiJC{ORo(8^v`;8VB)wpFj;<U;MRRB0Ef?pT&#w4I#(e?L5x$3+MJzGIvZY0x8nMMVj$u9k87b~Tya5QqWdx3E}R8{4jXpC?qsPWm8%KMYI<vY|LC}%@J3uvxHT>)yb(7PZWn8~1%D1Nx~~&_;s6$$^=ZaSe|;*l!kNwmqrCRtSZ@1oR{HI~u^ji`lzHy2d)Dms27hC?gTK-J!PO~pU7R479M?)gR&WQulQ;OChiV1+b9e2$d8(i4IW}I9llc<I?@~;vpyOrvNf&EQuoI$t%hF3@1AW3D3QzEEFv+aA8_wfVo$Yf_=c#KE6e^(;#WL8MfM83_I_T&ObSXN3Sc>l6U3fw%8BZ+tUS{d0#^B%cleHK?(F<o$;f$%5&tKWj$`sH*(}_(@<q32=TDU=kYVxFj@nRXq3&MD@4C94uatnkVA>YTmqj)O%^pSUkji4e}4j15|5m$uX%5s7`Z7HL-4L6>~i)<*2P<8xNr$=4L2sXYmPF6+=NM#QN$6IJ4jKC0K1O{r7)1N`k1h*`08nRS8Eki~#rO=EE8d%v2mq&)2LGET0*w*Ca60{#bVbU!V!<y*KS)-;6srEb8XVdaxv3Q^l?sD4r*7PBZ&Bt}i;zMj>Dk&=mv}TNv@pQMcv3lfYtTfcROsT(#28VHvtgUE-3NvXAGEJ#?f=${wn?0_3A}o*<4&fIzb>7v?N#=;Q5%?-)G`Z#DvrN0`X<$U;A?zF8HrhZQH?~dRc~G74OncJ|LkTp25&S`14S#{|pV$g?h2GAs9Ib}et|Rg@G=GLY?|h0>8hg^Nu3>x^4USe@2IE7zN8L8Io-nAr??t#O{QY*ho#TM8ED3j6XF5wG-G--vlgR*>SUyhx(EDD7O2A?P#z{N1{2}yxIyF)3>Q61Fh#c<YCpZ5STVMYLnlA?JoKvRvTy}<z`%2U~EY8!iPlkHN3M8|S?#bs|qztFQVi{s)$5JASb#PfOX>4~|`f-{0;@o|;TzLrt?c}cQyjJiAhT``M8#JP{^y(E4ldBr<#c1^Ok8gE{-@9zVI%<!k(^1qXXCnP-uHJl2*G49WXca;ptF_zbRA;8^qbOsXk9QsUcO~PSH-P+j<;~)bybESu8Y_XH8t_pWJo`8b8qxwT$yru_eF-JS)X#TU1^>IlUe9ZLH_|N<R+0=oBCGY_VH*iYK6up)`9!fEnvI<?-XosKC=cdRbVSQLT_ToJOkQ6JOk22&^0;fQ4igc)aUvpgPaG#G6P#RmZI_exb_@?ks9Ncy=Za9PzO~D~SzDN3a%A!1WKJ9>mg8mK&cWnty;{;EBr!`!?b-~UkKj^H9w$YMlosM_vMdaw6;GPtKss+UbTca)I_}nDEA+YUh}^u)t_swl#Vn#Aw^>d8%wjcR@hv`Dw*b=CosdawNL>3<Na+@pj<#KfR?%GG)}FNr5alBQ!oRqhM`krR)}LKbk&!-r;+UH;?X1Bz#Rv^zX&7HOtcv8DErD$ru<fOI1#DZwF2Rd4vL@**ek`$&wHt=F$WbtgI%z<g8%+H>VgC^pdEeDf61*<|O_071ji?C&1X@E^?r`il%?(0qWwewB9mhS>7+@>DXMZxC7;>xJu`Vat#{Q;78=Q{wqN{nfif1gS!ZX4RZwI##W*pu(YI`Q2H|$LbLLDmwSfbi8Q4Mf6vuzgag`;U8myhPQG;xTZt>)E|P`_Kw)AlauY47PW^0u$qY)aZW#>554x@fWL7Zk*iXnJ2`w1I7Luh%Mk#)UUZ3U5-t0(V&?&1o`Plw69Y8_^~aTj;mE2`e&_O3ybTP@ag<L%cFZSRpQPaRnNl_#AxF`N`5tlSvr{j4rtjhFSci48ttGD8aBSoaf11;vJuSex&2+lLX7WjQg0habX4iowLi{jxXVIPX~CedDS^aR_)Fy-^Sc8l;-d~ONzf*Qhc$Za-N=0a#1X)D%OwqgtC~;I#Upt-_>Ihh+`6nRiG${&3>9-9ICe-`Apyl(b+>3_rf{MgpHQ3;Y0c@o>7Sd&en2V%vREwUvRoinp;%?Pp!71IBOg+W{wz>2M+u-IYQeBCqm9K^0Auw?|lmTxV!HtgjTB)WzO$pRnf${K<Ar<L<DFk@+GPxAbmt1Hh>}V1?66W?;K(Mv0nP4_S-#(Iz9B`R6F1MTy|2)gn345<Zz)2iUq#3XGKR9rZ#XW=MLTd6weDI=J5+wcI3Lq>W<81RI<6_V9Bn69ja_eK@>yFY8<>Mxhsc4YFUlt1wm}B=wlseRPPlpw4z*F)!IT~E7%!byq<e>n;dVjW!~*DOhby0K8&WBmyz}o&N(`zHJqfiYe9_*QZRTGo5C_Kla{e5E@P6H=BD6P?2wozOGIXDh^-Tw<xgy>8T&;HhTL?cc(n}0Vs#^O>FFx%l%Ki0J6S34PArLcBC4X<7yr8vdM9_4dMBSE_FVKg$>NGnC&_uDORp0qAWrZTA;9R>q7dOf%AU@rc(ukm(3+E9yX;^bKpI1z`q-otSlZ_k`#W0fbW|N$XPJ>uZG4Ofu$=kUE+&;xqc+r9=dau?nV%RR-S{>g_|BH$Qy(q%S9EiwItV#10%1Tg8*=0WqE%<H?|`>#pW&2C6&+BN=T&pr5)zW3G9*i7NT$lLV5`({wH&xkh<QE*TYCvMl>2u?x4CrXS{Ip)0r$|i0C5Wo-fep|7;HdpH=Pl#K1D}=SGq3Ql?x?<cPc7gzG)d)R^~-s=H0R~Lba$#RYCl?Lm3%ge?=KqC~8tW5I^ovMh4d}HFv1nyzipHo-mu#80ntEU8AF>J^HuCS_Ee2d9%kme(lxqo>&1t?*D@6U3VLJ+57pcHeLt%E(&icBlgpHfC00rXVD<))#?8D%a~7+d)`GF#2K*N7#RslJxkIqY*zSo&@YkT6}fvb((<j-!9ph5tzGS)H9E|Or)e^<z%gE@<8>$OJ(>0U<UVh`$1nz*C<^D5cn_=CE5KAJBP=bG*=dl{{q~>u^0qWZkHZv?=6OCYg4;bja(&e1J9uQsK&!>}4!@A6_IqAydt2V^n+EA1obGv-(o|FPb{fsAd-9&R@){Ti)2)}iFrI?yS2f)O#x9rHmNagUFPo?}w?MPG+*ZF@`OB7gtF!yK=(d0j_+~bmMw8Kk62Y2{NR-={yBSKN@x2+4Y50TePVl2>dFtSD)VV~U2i_J+otFNBy!hZ{+j`l?mz&nh%_}WKqe4k94!i*A^8oAHfZtp6yG6fu0ptNzfe)=Vec5ziqP7sGmWF9t!}Qp|w7CpZn=!RDOgkE;7B^O4+FFKblQC^-m>%hvS~{j}9g~q=6p*@^fg}drVLD4NYxWP~d=>t~u&>GVEDr(UNFyi!tXzWP?Y_m`Ci5G7-QCBZTllk{5jztFr*jEKLz5BIc3z-G)RDWWF_99UKddtgPQx^tfMASn!fHRcS)8HJ59n15W<Wskep0jVcxegau0G_xf*=rX76O6k9g;&=5g#adh;aW7(+ydH=+l=~qFGxuQd2(>km%CSpIJCmp-w!x53w%~pivqC5jBq>OYew+RW@y7(FcX1t2pXalDt2h{_yRj8ZN?`xa1}2h_a(US9ia#cXbcoD8^@hk$-5(4=5n|AMy`v`JsJfrhYV4<^CM;VNp|A?o-V1{%9X-lfOQQUwP2L+2nh^*;s?0Z}Xo&@R;rw1JPhb7=ZloW6W19N+GByg?H<uIzl=jQlU?g)akIU|ABtK&4UnTNDlG(dxV%Xum(X{dinKRgkW^v8~#WZVKN|02878h!em6449Jl!)UOZXmwsP|qS<FyQy<+PGi+dgp;t-q>-jzIq_R1|8W7lUevcbT#x^&q;kn_G8ERH!^L>6Irp*@O2_-((FCJNx)T>k-vl`}zScs<<J$(>Q?JKPknjbS+3C*vWtmH9OGE<doawRjPl9^G-%vlMy4mwXyJN&fR*QRhCXs1ukzEMZtsH0z~W7%}=CgVvoBIPR$#?`^-2&Ml`cAj=&=HMSw{@tLMC#VJ=_MH!dUYK&h#&=K8E}njWeg5L`_^C{N#$Pf5J5OeyjaF|mQH22_nj#S1WZJRdeTD!Hi@$;%$0v7$ia#E`{^s=MtEboJ7l#+$p8GO)uTlb)m{{6_XJ?1czj=Ccv9b^SOwy;k5B>G}(7$sZCaf##y^telG$)u&gYHnY1`8qGS3&em2++;nOXLXP?2-V;`^2dD`>U5Hzg^NL@d8T}`4df~w3U#%A4_NM2JsCYmG+YEYz$HYTk~`j;?F0Gm%VCbFsd_9MQ^z%2jWls#BzAz7|y48+GjxqTzYJvD#mphjM|kNi24AeQ!t8xY>%#)gBCHG41+!1``{tvWIE(e-bbw!1I<RH?U)eG8Dem0OFp$Bo^!LNH*qi`qRyvboWYn>E3coPUx!TNYdYGxo<;GrQV7v@A4?mwltKi(q&J(mHTdyYH=u^$P~)?RUIx3aH0(z7dKe9c6Ihx-JIeFCdpBWs(+jRANmhIrr(^9Um4vs+jk-uaizD12)6(M2u5TtKA29I1NK?wWf*ZY7?X6ZVzU6vv^m=cSs0X+~Kh}*uP<+d~MfWCABgk)jSEcUNwD92sjW6;3-=r~Le9+%R{k&XmRs|x|*$i@c+#cLd=<Pzzx;{;^h^E{Dkpzm~PE1S6kH#SOf2KjaaSh^)a}aM_gGlhRYgqA0z67IA*h}n>jB$3ICbPjX)?zi=03gqT(J1PceIJ7K9S4)L&+kAg&a_EofA5Z>$u}@q%f5dX*j%`UKaP@7lB&Zo>aA!DeW@~vUO2G0ZIfczAHuld17_5t7}Sq;$@zavXEq7^BnNI0*zOL8t+s)00}$mB7&w=VAv=_yqgep%rqR^PF+V2EZ7R~*u}_u40UqpZZDYhdxvz`nRq9HO8wp#DQ81nm>_Y+-rWl+;ZhYG|KI}k^T2^DAx~TJ^*J>IwQQi$n^P98E?(3fESZ_Y!v{#^`1?}CJ<Rk;{Xj(KdqmkkPpRz6oX>Y$Aqfr{qS6rpdQNVK`&Kwne0No5{o^dRlj3|7-v!IJ!S0K}`>FDVhrL!=bBH?^OT0gO?`p&3|CN0pH8f)_g&sq{jf~f_)zBZYhWCBKhw<o$Jj+}s;8>(fV%BWg!==q`MV#jvduW6H+j_eHP|LCNHHMrD)bsNxP?tRpz`nP;?f!cOEIq*y$1q)D5hhfNfa~|*R(g9kt)#k)_RmoEiyv<f)tF`@D4}roBd2pbiv4`(f%VZU7W*rCtgn~ai)Y6@{Zx1DD7FIC;+@Vr!Dz&v+EVbz>)nw^I0&8=}$lNT%U5ggMd9?>S-IE%$*{^x##1(*T3$R@VxM=}yDnPTvFHG{hLi^lz1$5aEblR9xBH*AuCLcw1P1Kg7V!27!rT782Rjn~EWcO-0VxO*Wp_6o*skKcK5N4W*->P63jw9i%D4qCD8XxRwIqpOuS>3S)xg@Y(;v+Rv#QRNpzbV(18dXu~SW4-huwUFrt#{w4&QYM$2jU`{wLSr1E+Vr{Eh;4EQ@)57Rv<EBOWyaYvU?k}9^%1xi+*q76za9<H)a0qZTiM}KmBhbZ_5Mv=>ie7+1}0>d3P8426QlTB$0gM)p4te<l)7Q!p^BxEtgiCzHjP^E~V`z!vm6^S@X8F=3JjPmcfFOIVLT$pz4-ro1fQkO((=Qc3E{Q)u~*~*M>wQD4{Vb#w~8@I&FhJcp7zP)6hZN!Z%GX&cFR!dz_mfUEr;;qGE1+(OMzD{QqOWbBAI5nTh!`?RWmV+m$spC1nb}x#%|w`;#(7-rRlc7Iq&d`jUOe$Nx|0@^?_>g-J$N-*ZL%GxYRdLP=+|LMi?<mHZP`R>7bV#V1^@NV3+qmeS`|-jsT?)t36r=B^>7o~6OSPy~=L572{fleLjYJE)C7YkjF(U|nmg0zcC-_19AY?$F?6Ykr|wI-yIJcg=aFaBNb`t*BpX_RYOq8!#aH8iZO{#BgcOFsrJOI?-M}npQPAgd(4)Mt80mjKnDdzmbOswm*#nOjz*w+D_Pe9wwk_r|O`t6U9Agxqo^CnsruX`?X&*^@njbOG9+gd4BqB^?kUI;+Ex>@ZPzE4_7D_b>q4D@jw&Pz*Bq0cIVNxK|(J54svVh_oz2t`W=(|?$Kd~Rt8Px<h-=!HLcedi%Dp_MFbL7&Sr;qhe3fNZD$jh7(I0{?;=59q;U<mKqjFzo4t18#35;mV`QA^X2BrjOa0TZ5oIs&xITaufJXB*Qt9~Z$>BFIkFJl;4&Qi0H#`;+FO10!<93*)F4qW*>5{KQ!qFlfFM-ZiL2<5pGh70VE0sF=X&?iOQH7_&v$Mmu*H6BE_U!3djcB4Z1)&L&Vh|UhsYf*?l2&9@1$paNRKP^Idj;I#H7a1b<rTPVc>3xo9iTdDiqs`7c9a%!>JNVq#F4RSA9|ah2<&WcZ)(|53XOADgk$<`6dOZ|^_q0?M1$m%W8wDg$@$CYCr^*BU!Gi)9KhYF4XvHeXv6u7*Jl^{OwXaE<D<Z<qL?Vs@&wHDp@X<YSbQOXZ8tsqv}97?XCuAjeQFK8_SDbvm1I3mG-_GFjH1C#k}8=gva6e{Rmd=)bwwL!*iVM48^z}7ozBm)9SvyaV`$3c6e<WZ*Met=+=66Ra+*%B5y}+U<e@24rYIcsFqHFU1!h>K=2bvQ;2)UE_y?E=|6p?~SH2>~C6&AKon(+7g^EC*S1ms-1;Jc%s4q$-ajig|xqh)5H-jg$aR+Z+60=Xz2v?g1;JBWXUsJnnrCnaEjbPzKK$i$b7TUSEIVc_t=O>IMk`>}!Q@*tWuido#Xy;a>_aR<YKw#Vt;NN`!fer3(F0A?Zym25veo`B4sFR~0;oUjBNr!jGcWR!vS4U6oC@>4V1&cxp7Sw`;YQbV@3+i~8FK>bVWVAplB9Kr?YCZ1QxoG|<gBBKHTp&3_-33y2z!a*g<7p?nh28IFV_U*HUfvT4So9G2PH9Sg&Q);Tk3DdRsTE=~pD}B#-~kFuQ|odl;+*MZ^B5YO+~NiRgQ-J7yl<NTfszk3x&n(AG<)!y+x*Q~pVIOj-I3aL&F7xwm6&5Ry%IH-!yZnJ9&Cchy|A~CPv}b6`#?{6nGnk)IBm!$Pd2IMg;+dUNcTML17b=(NKZZafsx|ya3TSX4k2F0T3|^%eLM;~Z+e?}lQ2bEM%~#cNMS8vqaR+ypy}65qilk=Gy){`FbsOiv6G_v)MtQtvLGKs`0+tcwV_;3nS2;|XR_csX)QctWDMkfI$22XQ-#6^h&Hi?f^lJm=1@$?L3A=AjPln9@k_(^`#JeZViXAU4<%Y6zTZ<%=n1_-X;daa#NU6Q9ugG3r;?^GDAMLt80!}yw;F5>+R;YJl-E$^j6w^Fn1%vLVO0rLYXpS2-W{se<nOVmq3V@^Q89=R9yxE+u$~R<^#j=|s$v5>tiM9mn|#n-xlz@NsOm*j^>t8f;Aq*c`hBrgzh9?Szc04x_r+G}sB*b!%Aj5v+#WCDU>tQ>0^Lkt;BmK_q&*B21agdWGzBh2LYYv=zmJM2y|*Zdf-=1q%jJS~mMKGw#IJp1TNAV~jpkeZn<_iaeao+3C0z=uqY8r3MaHj+Uz5Ih)WHJ6t^PWg$XtcEG_vSD93@@W%>mINnekkB$O2bcZ|7*3hVHib=th9NB<BLc<uIIc6L}P%={eAi_W3j+eGLI>-X>vw_UiTFg(9eS(-ZYrU?{?vVar~<Jb8LfAm*Z5!ilKc$}4t~6X|LLD#X9VDM05>^j;o1(@8sgz?0{iC(YE$ReXU?SMv!3cgWW65A?BS!BJJ`QE9EbGmpxG#93>w=$-Hpoivn^ZUwBH>*0e@Ky2{mQ!(&(Rg}9x0Z*&H4jScHLDLW)J`s_0RX{xS`xEhq0~kcZ8ytB;^EEkx=y90tidr%=;#Q1pEZ4BZdZ7$~6Z8tttR!a}`Bp3s<eCGEAjf(lv9C)Zh9M>kL#&$V)BvWq$V-r^?*=MfoG43^p^QSK-|BlwMx_U5o<<WrHnRpmH5s3=g4VXmyG3^^<sqP^@5%SyQ8MSp@IPG><QlqZl4VD;>1lV0Cuy2@c>&~b9%UR~?L)=5ik??(gcr!Grm=nC32z-o&FCq)t$SP+(xqsXv`Z^_n^(e@(Mqan8dYiA%e%6*Y!$M#{QZeDM07-A`i^F?xgeh=S=pMbp)%HFRrZ8jA6Az|YmZ&_HTgrVE{i6jPd0=vS<O#%xRM3^6i)(|tm*kSlWFnQfoEBY*SD&#YVU~&S<+&FTB(J6)SHdNaQ9~Cw)$1ger-aQG#j8Oy3_Jze}<u7XkOw*4(VPOXD<&=p1(r<%Tj7;mPOneY=>3bvbKK3VPT4Lf+EJ)Hg7z9J}~dY3*FArN>-@<Khp*Po*W48xB<w+4~Ty@x2>3iFzT=Fx*7O1^ZgR;e6<E|zFIk<mMZopYxw0>c;L2_PNJS6S5@QW_M6PLsZ_`Rg&k(Tyt}rS>WUhkjnHqy3^qx1qsA=|Ik|20!kefYo<{R<bcRDiW|*3l{qt7WL0TftDVuP`DSHDJADDJ;Q0YPxJ6q&s0(F}4PKWDadO_+DqT1ZCQ6a4aFll+-eVBB&2rJ&QZbh&4^C!Is6xcW4i$YMumPR-7Mj*$iyRCUcdjUd@IDUG1@#6a8>G_2wlA=t0KKl06tLtZnM^B5AW;z6+rKM4?(18f0zGb(j+<zDUeY~kV-H^s(gEt?ur*w<{-Q3m-NLXsr>sPPO#N@hu^76v_gQt3uzcp2gZjznqff+cg38xD*1{<BZ4!lc6W&-2*C48S)ypnNFFf=pbeo(-@2yT_DgNdiL8V_DbSc#|Y#$zMkP7;PI(~Tfa-U%76M|;@ZC57_%>GSs4;W6+I#`mjv<cZ(jY1)Z<DGT?3Gqi!;TC+@HZNawG2$yf9Bsm5F=AH8ClQ12hVmJ=(c^dWd$jJIx!B>{v@QbfaH+Fu<endxHVx=Y7a28T@qOTn<`EV`hM5AcBXkgiE=#RIjU3C?*7QgwQv-}Ac!JYiy-P|cKPb$A;f`4kwn_KLkN*8tb_qJK{=dS9Hgu5cu*0ghv{UQsyeZchZU}4v1f-9TsK=CE6$c7V>Ws=ypb2F_-%#;Qc56`*DH{mGKonx<WWECHVQ$nbi5gyNiUIB)Yq55$>83tK+J!m6F*cS^Fur<ybMTwOks@g?*@q2n;$KM3wF{NF9k|eO?#MP=}9_M<rK9OO5Hr`QjIvQe#5y({ZEhA4%SRmk6FEm5pC^y}My#BAzjde@hHc~l)Fp`Rr@2rhsO~O64*?i>tzLBULr06k>R|E>3cXW8{g%lnw#KdeK&7f@0J0;?H&yn1(({A8hgu%$G{;JvR^n-1fVVFVQdybSoRW7CHK)jLnWHbu_a;yKi+kfnviQ@_1B_9gI^rT6@vt=CnBUGEAHfh=4p?@Fm*ie{*ioy84)F#Q1W&s(6<R`%0?OYtRcCHHg%gy9FTDVZYA@_tm&C-KOzlqsFQI0U4?kw&h#W1k0Om5~;YI`%xdn->!Ri)faz@BxS8FoB)?DU*MR4F+Hb)IwZ>~Yu~1~DaEc{l5U0*(=UV~;t@`!!a)kg3KM3o#((qmdk>cr=T~r(DEmwraMvbv>cTM>`f5sZC)^tlNdKSo4;?vl3HpLp00k{kUC<rCq>+1XNfA8po-FIC7})M6bYxu~lOxq_u9BcYB6Kb|o&95s0bHn8eD$SG$Y0T^d0vrl3b&0-0BR2K(k`Df}1sm_G-42D1(Wq+^(h0OlsG0QU<9$!wV162i<aa*A;>-&68Ahj4-qArL+47P7a{SvYZ{5|p<|3h;w#E1!0u<U%*XYVSWN?;k6{T_H?#l%5Y_%3cm^3TsOm^460kX7{$jX%)~U-_qDo&v<tZ6D2hEXiX!r#pagC+=o{at10m%OibVR?Z)({e2T8H764NHm|dm_<YEu<pl1&1kCLE4;YQwI95lbs5x{{bxte1X9hw)NO#~op;guhPm@Z68@jz|TI_Nkuu6YWV%%1U>btt*@LXLilIy^|bXVZH{VyxNZ)Y0UYX^SDsu57PFWL*DlwYBCxPq3}&Ju^Fcp68wU3X{OY_*TeOUZsbp`!#J>Wa55cyH~WG121r;Jj6B@Ogb-_Jx@c=ElNqnR>x0uXY^udhJ)g6ng?ZUqVWoP8gQFx+(o0&?jZ;i%kXAmlg40sR~v(Gf&nmo;2q8*Si&xb=?vQbEVyrHh%XtM6qS<>=CxTpJm^mpj5xS!G6CHkSLyHSQ?4^$>D$HcBm5Fz{?J|>7SK4PRPUXK?fZ^#8ud9O-PX=B38vsXYY&S6mBT`(XE56)h4a5Hb9&TUxkw|ivt1L-#P#~ow#jbmS6sL1xl=Vx22mBst7wl|__7sfn>j>{*&xM$3~J<fz#I{yEv_l5aG-i$zmKM-4yUeI+=Sj%eG-MRFh7f?b;`(rDNx6_O+wa*y>=awp}zw?bAuB;u`U^jv?ccq4JOIDdO%OL(-0Tcs;x$QTMtPITWxa>;`@2l&wU&9^YT3nR=mcB#?TC-0fk!BmT4_D)msX2xvMR$OB5nNb&YEyDn%~!jaUfl%UQ~=3H6<~{KOX9=2gKZ6=tMGUFS-jtJXY=AXmLfiy2VL|7;CV)Grl5cc0yrKX3c1)W((7QywlFrll0;fwXB({F{fE;7}s!*vdR~hPhIq?MzxB8{D3Uif879bJR`AK2=Y{ptta{5Um3^XJAKxu>qi2-6781AHz9nI@fIO`_WA0MDJ+fGoWmSL>t6z&ZjulWl@~u%m>#=JX#pX@@wq}oa9rPW8A#bv`^{n7SZB$m-Z}WCA&2i>#S@I3c)GJHcJwI-kh#^#5$@~#kp*$ZJ#xl(JEPQwbvVz&z-xj%1UYexib|P+byFi#{^wD!n4unI-5n)uu|OmO_M3*-NSGxw9CN>wIQC{_FhIeR!~XY6}1XbZMBmlpt=jy;x*j|&vTRqFl4yJ;(O<4#A+F?ET24K(aeCg{S5rEj4{v-QK;tAIAhiPs$;|JM8Ue(+WI+W+G=Lp+$pPb9j5$A&p3q!vTL;}{M&QnXR%iEufSL9iujTvd64l(bgp)hoOi=GH1CQnKWtAmi+ZU;UeQ*+)IrZaCeVPFpBHqNx<DG2!zMxez2Q^HwpC%ssd0D{Q9?g+6!vGK8Fhp-x-uZu!Kr@zZQC#)J>I7Bq8XS4YX?PIhkmN?7-{(X8LYi$<T6op_)3>w_t%2I17i&aoSR+?H%oV3f>?M3S|3J1Hl=9nHTwCMuT|dD+ysJNk1BixeFc_DtCcQC#~p|940u&Fv5GF(9$xng5&k&r2eZ+%iZLe?eM>M-_z0_)+{Oirxuz@orXOwQ9jk_o&TKjr*1r~7q>VRiev=KOK6-+yxgsebZEoM|AKq#o-dg?>SvVC(Z%4rdW=r^W1KJ?E@=_kstlRf-aub&Ioo1&bfH^mf{GzH0AlIl{7R*BLjevRkDRj`<B?h3VP{0RiTrIj8;BixH%a+b*eq+=2Verz0!vzCB>DjO?hl@I0Y<qxsAE@?}!M8N{#TxMFKtWgKil9ZWT-97v2U1{nyMUZ*=DIkkx5)gFXIiF51A2p7K}UGoej&<|L$+va$&M>=?-<w%#lwoZXN0j9JT0$VuQ3_cn+vlE%mmS<HKz}o>5O8_%iRt`f_HY<A;e548kgYTGzEXF-6Y9h;$s6_Ss)N4S$-=gL`yqXaE}^BBA*0V7Tts*^f-;=@~-weBbd3}_t;xY0nlBu(2Sb&y|XZjK7_A3S(x60DfyIDX3&U!6dT8!V#+4sf|psWnv+$R49-qTm8gCEDw$2f>Lg6jaRZ6fh?Co@#?d)-l19Q+=}~VqmFE{o8TPp0oiF0<Fim3UY0rBR4TkmO)0bZR*t<xQ>9CH`hCJ$oSN-u<Bm5yE<p20f<Oee@Qc3C+oGgVS0e(bJf?$%NhrtqO%F=lMdWY5y`ER*#YL8vcLjJtvc-MBekWxH4qV%_WW^<-<XK?)6ymZlf({|b{an5Y*?EXwXrrjk@rnfFv((V#p(%~8oqummZ(QdiRXt&g7v^)IS{DabP;yiS|vk%d&;X}0a6k3+hyouI<?-(`U&b$mzLu`Znn>s3i40?qp8f=^e$%Qy^X=m2;y3*Om`?W_-v$SS)hhg{qz5MQ%;g&?)0N)XB`xs@Q`ea@}Qxm@Ce62!5aF>iH^(~M;fEw3v{vf(;4PG&Jgu_K^nWq)bm?|>puYZkvsyk`fPFPQZ9=Q*#5T5{9?;xlyvSe{zA%d9z%RH{(jcGC%jKXT=2Ab9x;U+<LLaqFmLMMQ=P__x5Q6a5@OsJ7y$Uo4io`qe@yW61AD>2JUoH=u3{b)2gpDsr1ea6MU_A0;XZ}lJbI~8vaez&$-k6JyeP)P&OcM30uM=`qTPG!bTk)I64gO0lK$PK+<#FQ1@Fr<Ha=&4;zZz-?(eO-Fa&$}rHaKGif{FWhH7wYqnK5w^eKjk+xL%tcCE*xk|VqWwfaWVsK!Tlkz#NhliObJ7EC=3c%LdR~(hvfWwLn*(V;~rb)N043Gzz=B4x^4Ls;DKt{SL(LJ_146-&~eHB*S*_?h2x&-VWxWl4$`QH$DHG_7o_Ou#z{Rr(#rLf0pQN3;e`55<iaajc=_;a`gc!@N`lNgO_TSbgR#;<C#dcK(_oOHR*S7Ok9}e^`qswi-}yh3#!q8C^wxbN7PnTxOvEFDF6*NEY=hp}wgL+cRKO&0lLMEYy2ODan)eq`<WKup_R9lWt2Sf-dI@_;y^yJ8Q$9OnhU#FRZ$+R#oe;+26k3927JPwbgo}g{(KW>@?6Y_^6t9@RRd>*$K_0cJ8%Cq5!TV^n+FIU0ifB|UL|>Noa>2cPTOBOc>LuFM7G^JRwO4j8?-|~iSipM?<Mx&Jx?L_tmvSO;Aw~vmwS}F187sE7bXLqla-cd6vSIadtLAN8Y1QgIRxk5j%h~FioX!1rd^9P6Z&KKXC23gI1TWo|AaC84S4A&g-$M^0deio*xzDbjYY$O;lZ-HMtysh}T{i}NNBr85J6(=<#EDFCOF9}+f@p5!Q8KdmqMNzXqQ<3pQA>!ZF?qxpb|ddguM22r@f03hsl#tosH1LUo?S+m1r{1qhsT9@%wpS+bxX-M6?_&`@r5dG!{_t+7GoLa6XAAYMVXG|g-dI)XF4ERpRB2`0esYG)Ey-lC{L%6y{?M^vOk*z%z2`QQU@_)Z{tz1bTzjU-IGQE!9Xh%$!4SJRvtBvcx_Vdi2o?mHBQ*7J+X00Z{t6kI~rL2?J?*VEr9}NwePC$SN;BWd%JDp|5da3=<$xwjo3@R;!8z!y?z(9VN*$V_ZoevM3bBDUT;1EsK+3$IK4<~SL^ko$4C;OMtkeABuQDfcfze^q1&zAR@mF+ZnMk3)om0(0s7K=Zw$TeC`v(R&4gA5do~~TCdbJX{Yaj`UPuGzAV8<>+fs-C4%4n7he!ya1nNPpHNMcGi5_b)aIv`&_qxd9Eu*9+?y<sEk_ul3X}3yJAwj7?0s)WyaO0;mG*Y22-n_m(ed(7^se;hgtg!}#*eQr8eYstuwBoM0ft=E6Z?eO$IXBvE<P^S+xeecZS1kbzWO*GHCmMB-+SkIIYGPe2t%du7OmPWyZI<)}eXiJdd27iu-(1#}PP@DcJfGd!!WM5A>aZu3s6<YOi)e&QehTA;!J$25AdESB$Q=A@-pYTI+~8y}E(2uu)!tIuy^fN=UR&W6@T&M|9T!FEd2|=|dUdRSoJQ27k!WuqLS@I%R0QesW~gb)8YqX>A*wD(c6jT1xJcK<t2)2a?$)5KVUKUMJa3^I0irSUj^23Em9iINpj`9`g-JuU5L_s|`df72)%GWNIjQB%CX+Dr`lBFz?_rENzy*+arK!D_*Lp&E2)tmFK)+tSKJ<n`=1qebot3?uGSn@z<)m{!>rj`HpEmSQM{i93(AiwqYfRsNbA&ipqavbGk?b;gHz?I8+BMR!5Bq7f?Mx(h;b<A?(R!=xbrEa!G)AKn{XCxr>6Dxn<rbK?OOLnr?;u0%>C(nzSFILIhaHiL%+jb^cpLnYxTskv6S0?@I2-+P;oM$B{tEqyL@;mhkR%UagrqpGix&&OP?cVAqfpRYZiUd!$MKN;lI5H~4+m&x@-F3|;5c1rr?hJ9zS71HJ*&d{R#E58=1r-Oa_hA+q7&JoDRory<H9d0w=D-YY>dLyGH{7c3*(~8GRFB;@A0EY%^lV)`u%RJ`KYpQ6xGMR-PkriI!50!^=sN_HvJ+_`r4u{SYPv@)E%Cl#?y2Gg8S(lMBykJ!@tw0`#v*@mKoK|UiP-P`jzsIC<Q{co@T0{EjU#9rFgiXEAZ&ObuCYzxMf~8is(uti&MJLR<g!LvGgNGv-f@5$KVM{C}bM=Wp0%4(^tgbxcc2!CR6(c$Wy{@>|?1qnM);?_$aKWc+Tg&-!pN%#+9fh){rO@m-P4&<NF8I_Jc|E@Q0S~Z9J@dlPr4DYAAA~$!O%Mv*CW4jJ*q-4S3Y>fW98agHc$xHj<&{dlsVSWF2SKgH<brb`c1hd5YxJR*$b#4h;U^*J?H0uns)%O2>78jiRecMk!GF>+2OOHY<}&;;w70+)%yM*h^hm{3ePmYn&#K>H;m=<bWf5bXnYY;0V;3OC~RUt+Nnpm<W_X;XNS0w(P^NFAoSM{4^~JT4y;HTP8dB9u<0>h1KaT0)BPi8GXWQ(R8H~KYn?T3)Brx$7NNSo4`+}rX(f=B!&0gB^I*8+p2_J6k*F`sJWBD>T84&bbg93T-dmjNkQBwhdYmUDrJD~TFn)I#|2`pDJWO*f0c4jyQYu#T)(Z$M@pmDPb!Wuiq;UXh@Toq1n1fq`FP*zTn>R2J!R=~*lM+Q+mGZzp>?Q8l+E>Qj@YWYw@s}v4X*fQLw#|S;~qfaLOK4j;cYuDm5OAu5nb;(1FbbbbNnHJWdc1g=tL^RxgtyuAdYXsbQDZL`V8)CIZ^BdK+qfS)0_b<9)TW<SLfCam!Kuq6{xhpE#`6JFk)9h87ui-E@qd4-^&H-<s~0#HJVpf%dD9bRY{3KbEs^M0D2i+T{f?Lk#d2UOuTJf`D<!PIJafQf2O8;Y8NJTuG4Rd|1i{xUnv%;eo9+58#`+@1SU!A(bm?|itU+vhJ05)k9r}iIZw4yv9mDf;q|7YAjQ+M41wCm>=|V5%WqM-Q^+rqFFVN`z294pcK7Y~FX)gGR<a%I)0_@B>s+?(*(Gs^cgw82g?*TPda<ip1JSh~k39GS@9vJZ5wj%IYMW@c)7uVPEU`A*o4Z>(mGZsY8ap>Si^MZ#z-~NOF~3L$xC3cK|Gt2oCI+nFy_OTgU&r=cEkq6KpxN9K%{yC<wswW_cenF+C)ll+qjVEEN;QE$+X0sf!+yK}$SOrwmGjVJo_C26q2j?T7*#9egM`^=&cadfr~mm+{}aVzuCx#x>1infG^WY3Xdd>eZB%k9UbUj@aBN3`_j~+0_bkDee&wp>tok*~g7Zlj_OSZ%;7|YD3%uuT3gjG4w5Sq|bTYmkv{f5g+=jE$Z^|%B1^Unb@%qpIJ7T97(?q-wH3)Sc@J@r#wRpOA_xI2L@z4J&5yU8nE(n+uIdqmP?f8-Oox!F(OGbmh`{qyo95=9GReeU_O46ii_0q3jy?S~6^7RRI>^1!U(|_^0f?VoaF2+%eVS2t9tHy0|m&W6YFRcJq7Iy;2oO9kBW#GX{t?SVwYCz18R|9gGjP!5LhlEnBRCb^nt>$Eo#)u^JzI_S1MW9_h1DTjBRBFjedC5v)$<k263)h-O&fk<jp|yhpL|Y?jf4NlW=~w)Ifi8ns<z<R%pGeiPiyr1n)`)6KR?kfo*|{oVNi+$=r##)=?M-~mGup;2sP>4c*4PHR0Rv~rD9A8KYMf+~0GP+NrA*0(5%sGu!0ocp8CbH}b8khbTe8z)otWa9;UvJFhSpdi3&#z=lvgeg&pV8xF-2p8B{rFO)t#pI?DX9GChDdMEYaiHh`(-l#~}s{@XovGtkc2E6u&^Dh`WRS%bvPRqa};%!Stmaz0eV|*YPM%*+rLlLUg07RxOu6VEMDd<M#2>=f3y1s4$SaN`KXh+@XvjUH~g@KgO^L0%y~VwI0QjW$tS5xt>MiI_=r5Sl6A=Qb)JWs92J8@R(E{Rgj}Ah_d913J^a2(|}1cBl|=+&=!Rp71ZHlI~wQ#Opd_BswOxJ!9V^>rFfeP^J^)lF<qv$k+Uww;XN1%WQ)LsSCp$5@EG2~)AO*a`v-HvZ6$E&d`j#r>Yk$(3c{{MVP8_K<?pSB?fR+YSjV_PcZU-m5o=-`4gz3I?qaoo3|4gDS)qJGPj<8z5;kuicm;Of&<-~Asva;^k>?rrej)Bvj^s<+trajISS3qmrQtYK63#e35;Q&V|1ARpy4V1V7WcsJTPBWB&IXuvyMU();1;(>1f-f=L@H({{St}p+%IRGvuM?rs=w??(rS2gDF*g$6r``_9fLOJkv}f1%4nhvVT=E3?>GtuutKBaN>@UD$-5meBa`uDHVuEPl;y*?N1SFX9oiKO&Tb7w&~@uHh*FgrQlF%TNHN$@l|Q1lhjB1kWKm|6)-!L&-y+YWK+Lo17*vFtu*Wp4nxAqie*3bz?nPLU@RF}D_dybBaeAy2Kuhi%U_os%+IaTYC+Wnbqq@^_z=0kSzI`mcc_t>=@=N6{BfyH~?Xw;(adq5@X`RuXEFV%e<Mr&|?&Q~bw^Xw?>0SV3uPUVh4nn@QC_ycHxej6hD$y2}30DLt^7k)(mf>wcKv%6OG>+gYlvK(Ir3K*d^<7R$XYHsb)az%_^tTZ%f$$0YUPe$o+}3jZI!#w%C*WfA!*>J8rHtV>(E!901%yB}p~YXT+opxScsFRk)9NBd=n5!AKg;7!To&kS5kzl;j{FKXM(NX_JFJ?ChTXQppH~iw<0D+{)3dOT3gAy4%}oZ&M}l}0L3PtiEfOw+@%gKl$4}3$&rhEoox3f^(nFpUJstcqx-xabVM1b6DfrNbba5W?Fjc>}gzg4)Zu~*z3-W*uyC9y)iu6V0>I*XyHlp+CNH&V`%D<_{hU6Da7$^hqm*nk_7YcAMuD@?#Xhe)jYZ>fe+^2jH2UL2pATy%1$jSCuC3~P4yqJzhvH|$~%~&(*fAJ+c_j`1U=b(b0>tlKG$0IV(J9^<F#aCz-^2XyYA0nQwzR*qrDiuWuBoN;eIw3U+boOaFs>4QK?aB!xisLYSaq-P7??55?;>%uiBO6G?rpcu86*NUV(K5S1P@|v|jzk}@&HTdIhc67P7JbA_pA1E3sb9$cS+&|tgY97bHVq2x^YW1}Uw`o>>>_7V14%p^S4dAisKk_?y5hm6OlvtjQNuAumi{`J^J`=$?LBc9eW2Yce-W9l1#9_gH;U})GxWnkCmdu(XE~-I)kVH@<@9<81T$VbUl}Ax(yp9~k}4_sv;7i8krPdJ-?l|!y-#s65w}`WgIay5w@{N4i~xpnt>R+X3+0K0%P>?fEndH>IHbXf()nz^s^rQ@F2^s`)VV^DPPE*ke`}IFd-6w(`@6?~YO?iv@<&ZHXixmDk*wTfiTTl@eK47fK=OgOd)kYphJ!ThX}`k^n|Km&6H-(KZTTccO3il_8Fwz6JbK}P^d&|@;a9iw4X&0PPz&FhO=fAu^j;_f&%^NU-zy%!XRE|{O|(l>Ds)IPtDwVY^dThLWUj4KUJA!usn;=RdA53l*uJ~dI>Q8J#$IkSBN(6mD7%>uLsYLNgv=V`+*@9Ufb!)JRnPepPdr6EruWw~++(HDAnMgSNpB&v9d_KssE3|?ojd9GVc;-?EvP9pZLeVl!F0Ng#~wzt2i58RGX5(?NGiDnY*k?K-O6qEz8#R*EUj%)wdqsj)sM!;M3GqwnIQ<ie$XVdBXmIeZQM(qgE~1&E&mnf!YEUl-$H;TJ?h4?)(|<Dw8NA$Rl%PIJE3nZ)a<*fmf3OQC>x$(F+*0Fm1$O6qi=TXq;e7%ac;Q!@i>~664EkD=rLNUlI}3<%|_viB;y_T2c!JQ{q@J2g5zjpSZj26_LLO-sI#DuCOI`(t}H`YG6=%!Anap6WHil(lcP}*hh?I)j7K!VCetPvrJRCqwV*APiXL49z>z+WgGn|_rd965oknzJEWT_JcX^j)o&m||S<@jdL$5pUK#yp=4;QcmDQ&^uFWt^j!Dainl$=I2&4Wt7R?gbX-7HzIWD#S#c0+PiS$Xx1n<nAHej{H@@&|iCx$*5%f-%)kd&F<@0Yw;XP>Zy8?#b6S9-3iJD5%N`<Df`gazb}$#tHIG9tuR{DnnB<hY=FdX1HBm^~YxcU77jQKX`vY*P;<@3xC9|#05Gva2ZdO`4Jsts_h5E>)-+2Iemc6YUAtp$9tx>`di>9^cShXybj~uY<%5K!hRnO9V+Ta{wjqkuJITd7E|>S137{W824et<(F6GTq)~Z#+c|qE8z;3g#y>Uzp@yFFFExatn(Iq2>MJ##V->;QCMEm5clyU{|Oq1ccRHxh2A=LWN6Db1jeh%?j(rQb~hQ1{faBKvWk5gjA&#zCIP2uo;1wi0z{LBHD12fW?__B8JUFkC3UK^P9E;{p?+*T6tPM8uhsPmavXM3Z*sA-6*I2I<jFM7N-af)qmkS<adReg^rH4%E)HXqOZh9pd>H}|7%Wfb22;0MDO6|g@+erjW<aSjLeeF(gf=_MZ?rH{bv!_A`fQ|X<3XMa4=5I$m53;p!U{w~kOphCsGYY+_BAI@F#-+m3phTlN`0BTM7A3qxtfWbUz}(71?~yGQxG0_a`qyKdq#*@0AG_m307yzys&njsovRax{kNo#O>`iDR{fNVqZ<yWoblK$6f4Fer9}be&%m0#wZ7J@VROOY<rMlv`i|l#DBmqPr@nQ6op@$>66Bl&diU)fwj;f_<Dm1kae;e=mRT@Yw;Mx8+%ay{J&izE8`%ECc3>ptnLh%9oHBuYFm8*;7bRK5iS!x!<&5NVd#>P$!o0G{^e12hzYkrAhW7P8M)=qe98H3@carsi*((3f}H!x!eYq<%W4CHVR*x0VM{e2Z}Jk3qxQMj2lE82J3F}lSYkQF1xh!~<<}Jr*1<}L0)f;l$ulpx`U#rd+METjtNBVIT*g^rjk6?tNrz;e8fWPxmQYG#7p1-eql|B?^&?*lHXGhkDJ#6wGy(N7^v*H(awh%b_3%sh;Ut-^DKZG$h(W0k*yQPtr{{*H;6{sj1$&mSa2|c_RW``Gx`I;UMq3>A^S!yM!j?kwzx@4wZhP=5If<%r*bm`nLdYw;3}LgXgT`DqI{)!sJ;3t!pNa(+F{K7n=u;jJ5O-v0cShkWh2yq*^|fBxU;g|5(fd|>!3vFMbUxN$|LMQ+P7-gXgTt%yaI6(6FvV8GdxECGQ%s@t9mcbxyv3jx06BYf;SwEg&|vV;dok<4zh_}L%rXxzlfnikjOAU@G#O=vht=~ujv})y)^rhc^z1JcBOqGPp)%$CHjT-0SqI3vJXN<bwAaSKC+9{uI3UA{CSYL%bJkDg+v}CrYv;ru(0iYWuw1A=Z&}6KT&!JMtUhQ%$@^AO?yWC+-N?|h8p9%EMpC-(@Ep%+EB#S8r@0to7B{PSTNH1X7N=5JobVXC4z#!+Q=HE_Pm($1T+^cA4U@tZ9Ney7!iOvS3QigxN8@Zc;pcUnhEN)(YaPqfdr+uwcGMpQ)4O1z0ydWSw|7DDK3v=e3meC9*0~E30Jkxu<RP#&hLonZjpR1GQ!@a((2-;m-f3{CK*jVCl7sB4;V!UTr$J63`S}&|o`VT<v^07?k9q-NwScjAoehINyA%~aCbJIeY!$z3-f*4oZ+&2p)y)@du^br;yN|5mKnHKHIe~d^IgS+lcT+knws9~|tcM1M-bZ$Epc$#f;(AQ!A+Ub{dM$WvMIVtLeCDHdk!vrRoyw{Z`h+cvl-HbJ_FYPFxtMM@Jne1+rHf%NV!n`gjG^VP1MdlJ#f6iqS~s94p!cp?xzL9nLG@)r6wO7Ycwy;8w)e5-8B^7@i2wTk1YKap9#-;!{L3_d7o)&`_kVbZlHlR@^C;Ea(R2%1FG|<!B0%ar<bqoA1A4alw<ID`<>-y~m;dtrreQy#-~U&o*t~Qye!1TL3xG6NeR%O|y$cvxQJQvK=ZceF0`kRQ+blnkuKgz3SDix8MtFM+b4K2N;Jt&q7f|PybSqQC>E}LNqP`NaJx@IqZije+K-P%K_Mo<nba8Codcm4QLRlN?fjKO_V9imnN)yios|SW)G`0*J!=q;n(Q{Ey!r@7y^nBbmXAn2ZF{r(Oc)t{nN=q3O2LLd-He0>GX)M<9umq-Hdq`ijb<~@U7P3j@CP=IGI*OZFR_~_KlrJe)?48FBY)8o<*Slbc+!x^p<9^|OPPbgmC#!a$?AKdozutPBOpPl}0)d&kXSK_)FKf1lHchJ)tl}CzGoU1mmIQf)r|~+d5q@3VX41Cx@M9SZ{~Dz*?n8cqtn?Vq^q)13@w#VAlM8UV2zX;U24K_)3XsMQt*49W5Ni7|5U%o|L}atk^hb7OiF%_D*4#e49PZ=s^r#bb-+NgYj6n^^MhkD6cz9jM`^~wRB_m9#ayvw8h)k<<zmN>U>AaA8PigK(j(76zvag~`Xz+VP5+m}txJZ4V-+QJ*&9nU3xH}O^VEiQk;kOR-o}%)Ym%J5h{>s?RrV=mRItYYqKo-(pu88QL-<Z;yr@dO^4wcw4l3=ld7@(Np4Dfpt#-SmgWL^1VC3#;lZ-RlGyqKGAc2Te9P3O~M1X7kr%hr^rXB?A<#<6E;OJJx(j}dIiRsM^Ow$CMVl~ZP*<LDROi*Jv0EANa<iOXasfJj-*c1U9Zg?YRR0m77H=#FFn792BD$<$DZaicNQA#Q^-rmy^CPmY<+0~Z_#u?#WFEdF*)RrqCfXn^zz0kwBnv3~5z^h9%|_-VR&Tf`)*A5dUlLE9=hc4J>(;swF62Kjr<DinBG9ruJA<^|^GK{Q<q0U^xPI2nt%TzrQjAU8uAqW&~T1cIa?f^bH`=(?YzfGPIvFcK$DJgJEXlZLE=LwXbN#Q_aLFxSd+q##GF0bNOg!o>>22jMGAu?4mthfR(aVkkPvd*6~P(_uQxR$9=p1q@kGTyg{jGgvUf5z+;0-d!$sEn)IwWQERUCB&k2Wn#RqYJk-&Cqc_EUhQ4tH=N6L${*SZVfTy2Szi(=O)hFpE9xGiKOe$0xn_4{M^fcwZ5f6ss^T5o@PAUR!%n6A&eA$qgk$t|e>|<|;rSY{RE>fz(Eq1?@X^7BCBPkobx>B7Z2HTiBw^UD**G??%|1_~o-sLkH}!Cm)q{LemW5!^<wVUZgTiY+t~~+@Ua?28rl)8@r`Q5!^@PKU6&vBkGjQ~z7=^~{jA$xd%?P?EBI`q})_1gZlsIUGagty=cFhr&uld-pT(;h`wsr<%uh`{jP5A`bPW~3_ZV7#RnNL~xYD!s?f)r?NfNk$JdGlQ74pQTBk&J*$%cvwH@^Jgsh{!{&L#>+H<OslH;x5^)x`eyc&S~3P_SkWK(7uj~)IIs*zm6R^(#hDu!eN&Riyhi%{`jx7+-ty`T#H!jCLASQP{e_x*O{+L0@3Y<nZ;ho%}{f_gG~ybq$6{qA2CU4$C3$+hLX@`_}8lCkN?8woQN!&O;9b(uH!K55v8qT&2s@Dk2T>L9z)lurT_)~APnWP=Bwx?#XGw-&s|%Yh*@J?Z(+lT&5{N-z)yD%#uTUf8b4o;l4L^ri7lqD#hZizUOiu=NkoyhCSm%ge?}M7M0@X$Q?~;;x&6-&VIi}iFuOs6LXg>G-0WZ9lAGx@ja3`uJ~d|`c}1bvUV?)5ao6w!^D!blsl6=_!Ly}h;b!<SO@jq&h3PLLBMU?yCO6}PX$@oG{D6TIDM8Op^QzGM4uvJt8rq*=Fhus<RQ*w(T36bno^W7}?79=O%N-|UU1E{aEcY+7Y!+r7>O{sy7T-Qyz5ijrI_z7gMsyufUb8)kH~RfgZF?u~zD0Cr*Q7G;YPqy8lLzpl@I--*=I?}2K|C!BPKk9bk4{Op1q9PPfb$LFjZPa3@;{X(QY6hy#k$)hVv<Bt>0OCa%)00U#mqeq^`ah4!?8!3w0#TM)Vn|o(k-!SG+llrNN)dca%(NDQt%w6!pcD#PY`mil3UE8oLM(amNk?FA>lUnrl=C@Zz~1!h5F2URJ{PcL3$N7$NqAX<dO+G7}5;K^*GG3U=Uub7n3O)8*2H32Buyxe5K;M?)fPO4<-|kmq){B)Prs9&03c)q!-DvG#Q_x;&X>903bzJ1u@MyH=k?03G-_WH)hIgS?$sA{V!52rSLR1c{f%%Chjwzf{_1c42+1Puz^4F#RXc3w}al-gV{7;S1p3VN09#H33g4dOUu9pCQS1}(5Zejn59sRzU1YoL0LGe8&-KLX;`j(s}ER&&s*6ugIr;2xdX5|8Fw^Mltcdqt%P>?U0z0<K5NCy^KM7SjFNQ>CF>}TuglBkN7H&y>lE8XAsS_qKAh2Z33aH9qzyqYrwqYsbfF?EsiKw2X`&Y`p$L_;=t0HGs9|5yS`pjGlrrPseaKOxz5$w_-=KPjPkg1gC~fRJ#|E@<1BuU|mFZz$MGwqig&1n9JVor8=GU`P?&s1%LVxikrRtft4l279ZvlVWt%^5qA5>af@Qi<36_M5LKxHixFX|L?5<nW;6}sDRSxfTjU6zr&36o^Bpk~lT#|)ZMYqv0-QESKBtziT33etgau2GGVHZr?0TUuj8NEPz={Nl^(2GboA*k-%paZYRgjcF^NB=dtx6LzJWZTP<)apH?FyOj3H>&}@X-39#Jf&J1!<q`B=G*G0E!t7C)JW3=|TS>hg^$PQY1*nI?I5f6BL0ES)+HI^@Ysj|MkVlVem|_YuOxZ0FY1ka&=xj;b6I4|#;laz>^$<wQM7Jjb>>R_4=fV+8ok5Z=s;Ih9{>LfmJ5xQZoO;Qu6QHGE4q$#e*#SAr!ZZh!OBvSGxQ?=KGqrfgr1w)@9|NeaXr0hHT>6+c2dRjN8Gw;t^GD4t_;tzqJ!6(y9YN#cbrk2p^1Q*+vUWmKL9_3UW<7KdV%WlKG{HDOfN<&R+Xt)uTv%Au%MSvh`Em(5eexGj<{vGz`G-=}Y0^p1rg&{M*X%68xTwHo@YckVp<H=-zpo1z$)9%II&_N`F$B^2X=$677I*pHk5_}Nj*$Am-RGj_5jMXoZ2XLK-*E@;>EboeB{w%&1IB43+Fo`Sfw494?sQe$T87O^G>EG|eXJGH!2Yi0{p5*Bxkps<KKkyI#D(_YW&3Fq{|rqsG1;x+UHwPPliis`R@S!Uss`=V4iu=i#iemvCM9J!KK%5I_}?#$jMc@o18Z)S5!T#RavgR2K-)^12oW1OboY90=1VevdEzX`Fm$M+sc6c105l<tet`6hTL<3hi3hbol+R+Hcq;B>YL0>WM$=K6>b21=!(A(U(eP+5%G#{jXnA;tS+}hF_)TvjKBv)yjQ48iTi)f>#T{!}Er->6rI*!STkByyw#Yau<BADpnhs~<4o9;p>cqO>g-U+<C<22O<5v|CkHcwDSr$D^z|mIqt0GP}bOzg(ugYU;S^OPy>?tCM75k~7S8uUJ)>&CB(_QQ-I0r}i85b^~6OS6lr5%LCe+v<^v#v4u<@DsgcqoJXij(>;|KYzS%M!gXXExazb)~9c$m@k8%m3CAL!H@ln!7ubDT#_Wr4f9pcc!{AP5@h1vHtWA4iM2nWvZ(j1Er^-qiRQ#6VPkk8$nLO8`FRo-ZZjlGC56?Nig7m;)a2YW6{9sf01CUkm^qqY;8|=?YhT}fmzwx^Q5r-=-WxW3Ja*RPU&kit47tlwKMIu+YB*Nly$CU--xf1$GA3>lzn%8D?M@oa*<(xBVrcA%P`;?B-Z<0h{dur5SO(y<y~Dj%$FvNY-2LAk#8Q6#>}PksX?|WOdGu0Tqi)79xCf)-$UN)r0mPjoZ)385W*g;{=?+9i<#muRpREc_bi&$FF^bBej80aG?9@v9qf`8R(veIv8#PhjlgT+RC;@Tlk{NH$Pl?jGxze4x+~C*F*<C|H1FP9iyupDxO%vbB{7+xc}FmMX>gG+fR1@tY@d(06ckFf&ilyYrT(gR=VK6F_`{6hEs5yK&-$*jv*tDGn@JsQ8B1>$cS`S1cUIq>?v&q~7IlkD)2frEEv95>+{0p$k-|h>3}GF?kZb|!Lxa$WN-qw6B$bxOpI5Y$Kg1G+`GgDcL9kZk4nt4=ov@4ovO3B{4)H+01t3x2txexE9$k$=L#4u{TP<Z!%XqNH6&Pxfo>_y7`Lew8W)FS?p7<7XXBSN)nc&Bzw;=#SodJz|+@h%IK!0DpZX~3js!T-QtHYD$-yS}HdahzJOE#&_ap_Y9VcmiGcI&;K@JEu}HE-VNBH?^}EmURXQB2-vorlTe2m^zo;EB3<>}IhGn@wL~JkC{DLIAEF%p>DAyDaM~ETv~`!nGZ9NgmCnhk%H={R5rb{pFwj-unTO(AEr}-g<mpdv&=Z^pNm=P$l{Kt>ud&5Ukf#1g_K7aILR82H!;J<UI*-O4;3t?>4;3-(sV4eeZR@Z(ZERiMz(!;OTC7NpeA7p>Q^lK8j14LHeFa`j7t)lky+`gK3BnG4_R%@e=b7fsrF_9V<1i<>fdE2`<z89Fw6WpKFE8UgQylCaK!(!tR#9D=K0^McW%0?jDU!*t?#SYe&18`%^3dUaSi|4(8V%*l9#L8`*79UPg^L`S5{bRiJNCW6O4Q8awZS#UK&ZT4bZvZoG7bB}}Vgo)J*VQi?U0Tfp~5Y(`nM;0*fS4kRlfg^?-WfB6~~xfRsQe=HK{-!eF%3<oG;9dkfH@lYxx5k`d{R}T{_Sk011{iTZN=cF?Ef2+H;t~QP&{O(^d)}Hl|Vk9JShZr9Wn6NQ1i{y3UOJF1oFhSDjNFy-W!{5mMhJD+Iecp%7AKR+x?wP*Ls7Hpilj8_!rmxl2-PP4q^|8EoxOqWip~oPc&RU*ePDGk-=&UT`pr-`Ug7e`Notv4vb#kP{16S;KuY|b|g&UGwK7s6JE-c%g%MgPZx;yXoi|ORH+<^~O4#p=O1s<U#Cb#p*!ORf0pcpJ<Td9Yle(DJp5J&zbZigVMN+F-qF2aGWjVa2=l4t|EKOU!2jf0g&i7Kded{nV1>i$4e^&8t{vhm^LN|MMF<^yaK$O6eV8E>U656VxaYYf?<V!EYtfV~?nZSi|FjpY|CwL&p8!{Z5U=YFN?ae!#jM(uYCh<aDIOe`Y6G4mJe2PZyo^8o2F34$JM4l>%_gs{ihbKE5Mkn@JoO&Qk3?d@$(LCgbzua^;Zn98B83SIKc6YpmzmP%->R2E=sTV7pnHdh)OxbG}AS67$UH#Qn;N+rn+63<Dvo6F6O<&D*~=EjPEPg5*{MqyXA2lB^bN#z5--b;|4*nu)eh=k`tg#Ngtl{hO_??{QmjtwZkXP1%-=|$jzdU^LT$*V^jd#09`UT{A5mY7jDtD#xvh{JUT6}`NYmYIg6676Z!Fm0noA8QC=j2_U<nw06>?*^xI<*j6_GYF-|GW@@qrq+Tdisbd$I#p3mJ{nRL*#XWaFh-kUloEqmi%R%R#%OII2xKy<jb&ws)C}kczPhX$=Bg!slMqiL7~*In$&qxGiq;}2fQVoO5wV2A#zG~G6Fx~Cpqdb+IhEuKNjMTMqY->V?d<k5uepliwi%BDWba7?l0`|mtu<_JEbGa{ABHg`VIJhII2e@4<V|%o#wApWh%dxum}MY6_!q$tj(CY%&Eor?Kiqt%*1V5T7cUl=rNKBHl%*6OChXOzcE8Lj(u;mjWV~k0dvoZK-qw2?62|!x+%@8dM84~U!`_=iq2beHBN7T!E6Cs)Hrn&yJ=j7TI%-k0Y7iL>O=Cz~Saivw&Za%)3<IY|(#&$LgD^i~Od;!**<s8dBjmg?{E}`Go0dq36x5mN*hj$_M4$o6oV+t4B?*RR%9DUns!7F$DyO$?ib5Mi5|p%Ru_cH~p>=Bm|HF;3vGr)irHNcO7Q9KH7?B)Fx|y|eX%{NRE)|l?f;_pR2qwq_YOYhcbIe7^(}ZNbk`X`u&dxUCK0J4H-H15jzU42i)4lzdJ8xdKPmgy_c8*$F#!M=jdY@;WhA*2a(#0i%dI8&=#`y*}IJXUzm8{<D6xVnq`n`Ro+>_$im+B=g4MkvKf3rk<S+_Nlv1VSr<Xn6xJR&P^ZEGGac^tAOQP8UkoWS}>^sa*UxQ5(eVS)W2_yoj|binZF5T9yVV7_xQWv^t(LMmNJ^Q*NuDfoSv)dedQ0uQGZG8y_Km8+nah%#>=V{~J=^+afN-z1v68KGi@NyOw3%50Z;+bD=HoKyltF`5#&2mWyC_eJ9|R&(-t%Nz^wDp?V-)&g<mkvkxY+A~K9N>Uk#V)RJRJ>y14<2;Zw_98g$An$r@zcW!oan6n~jCV6v6pIsW3G#x;v(oIED*h4`1Vt~ileVIOpB7^aMDKT)T_S~jo0L>-UeTK((QjxNe9C)?==>Gy{FSBiSE`>@N`R}}3&J!N@j%*Lt0#{Yh&r7{sYki6erWmE7<Px*!g;%w;b@|=Ew!gQfn*|{ztf`9@pE-(QhC*mKQ0-FlCuMdNhPRuK@@h<x7gA|qX5O-$M903IQe{s!%4Y>@8uhGHJun4O0__RY06<LA8lUc0Auu03NdDiuE?E7!PEm85l*mU#ZwM*o&y;s&ue8H?3I13AxEF_p!leL7Txb-;8j^ZWYOGG@;#TnZ#s}t2>zKgwjCt!kJSoA*r^@);cyn2(!-2qd4`!QypU|BP%Omq%$|^*Fr=8rLXe^Yy=e(WM!yO#!&#w3a?>dqwWW%_1sO{!qd8iV(^2e_Dj3d4C5$UKx#NQTZUzDD@NC)kGI#nSqb?Fc$Eq$Rw&R2}e#U{~PPIVbhWfZR=Won^;uDKyn0VZdt=fgGdHb|ffqk!*63nw-n^xDTbx_N+Y~Ed;`x=nrO8#zZ>w>Z4%2np?x@t=1nXa@qWB1MG8)FAfz+F6kf8&+UP-T0z;GJ>xFZ-IPf6ppk94KWzNsWAbT!B>7J@xTLoJJ(Fh6=ifO*q1N6cdU%{vuYJaS?04A4*PL8ILh@>Nx<crt*F%(PL`}tPiULnQ5V?vMd83`s)-gOBg~&`K<ome<7PTR@mPq{(BjJlj(D#N-W|{ZbG^;_ZXLZ)$Nqei6a{;i%a#z<(0>kFNHCa!n4fB=WHzJhNp4oTROZTqtOM3E7UJB@0L4Lsyu1NVsMHlW;eigLn4-E!pzpf=O1MTA$%81oiU!`&%8zNtRI}m%If|_p?>CL{!6?fD*y$gt@DswU*}VlAmXRX%X?br<#M6at*?|<S~vd4d)M&3g_ZJMQ#s&G;8m4w>h4Fo%oQpP{U{>eYg&&?+Lfv?xpT5ASF3TuRbQPy0y*^0*7v)pYhgUtzIQ~I<ZS!<a+p;z-qd{4_4Dwq=A3!5g~8zZ>$vJEHYrVfSuPH7eOmeKu=SciDu4e6%0aDo+99Y(_VYW)Lbyv992$Wm;c?~5A$q1LmGd#t{8*sHWE~CKGe_Vt3`~&rnKF+C`bx>0*~tw6U&^qwo|(Y__hnMmiq-c=gB>l>N#vwLom{FH>|}GbXeU>5Wye|lsn;KP(CVMlpRZA3K-s_u7d69<qWImj-O5T>J|=gQJPelWEp!eM95?4<5=6X%hIc(-s+EH#1Ifc1E{2Skg53!@N{6L$x}MWu@ib7pT>EGJl2!$^o3D1t>R7jI`3tKJmLlkqjpBxl#h_0H4jYeVHG{|I6BP(APBCv&@4cNpQFH6cnYcNWyq{^C&R87|?m<Z^ql-CA+%HCmB$n9&(n3Q?`<lq1PdGJ5+r!fYE6SO457kX2rrZPe(lmd~>gj`zH@6zs*JB;X&U~)`*@+!xwZ87Onar{C8wSVR)ObeXUI<4owBM#v-+HZ{o!*#_sr7bFa<zhHv(}uQB^U{N^~9)qErt5>KQX8;CBJIuUPa69O6Bv_5{~js0vQ8m&pzI<Tflp-oez&LZtd4O=f>-~&yBk6+;!g3G4+7QOF-Sq&LaQf41i3Rfgcb2k()rp6Qf~>@?gsVvCZ`eld9F!YJH}j&IA)-xvG#XkoBT;!(8z?dDoOmgO!|6S_Nyi<QD!vS=p^NM23wC^p`MNCT>*5EAW?;J|%SetT?TC-E&YYt+jZMZ^E&o4IidFA2WlJ$J(Rfy`_5R=xb7Ck{7{5*kVLMP=ZgWh=McSB`noF57T=%_0Tb(7YzJiZvi3M0(4afV}{gr8RBuhHfw2<S1+c0layq~!5Do<p|L)y#oEy*^2*#0AA28F@G-2U!`Sb8<?nv~C)(rC!xJn+QJQuAf$PEtNplxHUQ~u}EqnRd>N2SutJTAxl&Ss-CkR~scPs)3TD$epF1uQ<tu?pAGlG{OmBq^HmQD33sV^+Lr#Ko}YM_1b_|W?Xi#4ih)Rx!gsOlVtw{T_kT77+v%DDdVzG!D^hTnOM-cQ~xS*o`<p6zZw9F1`9yzs}V)wdk2!f7#4!%NJFIdMyN!N2P81f9YWH26k>#`FEoR~R|NW!+YN4}jS4fWG9o6{*e;u*MEXhr`&gyRXx~MqRfL?9c7akU?rotDZ5mAI*J1;N@B3cof{~kQFZd{&_L>WCXJ}cLm#vZm28u!lu5N&Li`anoM*<6ZzL@{Cy8lX{G+>lG|XwnsO9EsZ}dHxmBN;K#jY}WC^agB$Fl2)I$_V8u3e%B#tJshfwb6*p1f&cDPfM`B_Xu4bOckL5g?r?<W1crw+*I;%=*p)JTMf;tR~ne&m}=jN}lFW<HK>?nVP>Meu!s4vWqp(R38Zq4#A?wAP74>tZ>Y%DhQ_GTvSQLR;Xqy5nibV=?}{Cn)K42@e(~Rxpw*9IFjx9|rqwlYM)de#3VaqgiC+<49eFrAZpqgUDXwle~`9rjMmnndXTvPV6^M{2sG60tsbr|DbuYv!@Qt4z~Ct@O#lTRsat^i{Au{YT$g#C(2bZN3PH-inL3;;_du~zuAK#MLCWAJ=uCruGJzWr#)lJ0W(yjJXGbf{_JU5Wip27lGc9v`V=J3r~FI$NLL8v46%dG(9ucf6~bNbQuKrB9*=(Dy{6~~UU?5YaOzjYqzhrLr5gnZoH8CZ48fj1)3pOvVl1`lE3xD-ufz}d)4~Y^HxZ0`(GA|Cb%Kj<hziC7=;?GU>ANzr=T2_V5mM1%ZdV&DB165Xr?CaUq`-PBE53zQ|1g|f(x_ye83%(fmT2g1wzB0mR?`ugy0do79HCSjujaV3?B~QqPL4;&VRYd0JL+X!_9$1-z&fa|=;nZP=(L?ei#QpjS=qyxIUKdX%{`AYd+(xXK$qJ6KJ+z^X8N!2#&v(_V_8+qk-I;LBJKNwcsu|8K+T{YCCk5DsAc(28_t&hMs2O|`kFXOQ(0Y3NjEW+@(AMhQt4TJuFm(7Kb#TTks3nD45vDW_@in!lyeJ}Sz#@(C=ErXUK&wV>4&O##Hfv(tazp>UGN<L+rQcQ{kQ+PAA4AU7_ZGjEI;v%0$h90I2<>-E^Kx?Xymd>cxI2}yF?wotVkRYEwHl}N4u91dI9SDNQv+<CjsV*iE4k_d3CsVy8q+x>y!3rd*|d}zun4)-7XSAdUpKi-00CG46Lde;pf~%-4(DRQO%76(p(XGTQTWoU&1R^KjU!Vk8i!#<F3y+<CuC3Ov9Oog}#%o$yhAA7xx$WE-lc$LZ<KMR~`GLTTx50$;FgF*B|>`fq4W|?iB5}Ot$ds@dTw<3>gloigyQhPSxsJP|_&uznL=!)oiYgoSrS}zpZQfZN2KLS(11PH-4`(4q+mA!w4~dhC>P|@0DAK3*}>T@XU+1m6cja31MNx{7>g=GA_K^OM`O)ZqlDm;=VRkT!b8OrZ7u^rI-HVV8p6V4bRKHoh?DR3}0Ic@>)YX4XAPJVOWMY9?c3he!=)jJ}?T@{r_Mjt#W7&^JXT3{h_%Gosv(_qkhja^-TwJO3lbP5xEpE>FleJgMQS3z54s$wi6+UQtJ{5>B2#I(`$|VF0vge1Qw6|=>+!E-FV!8`VJnV@Xmk!<Snu<Ei^Huw-`f9jS+7yrB}f%KY&{I9}zeN6%EP$!a~6Cy$0U>Kpg+v2q-3AsR7$1_&FZQ6H7;OAO3LsrcLuXdDPzj5u}6t9rbBz|JD9(yQCjySn!%8)J};=rwknVR3icQf^&b`kITlH)=kAbL&-b0LL=ot><Ek|a0K=|s3G7G{HQS6!>FkMf#N2}wX=*=WQ|OvN>SJ3WYiofcH8|m_13wm)~4M_I$1SlVke4VQJ(g~2qPl9V>4jeA7>mGR7T_8docIgJnm30h+*Bq)!=aW3#~x(rYz}%lH?UFW>NA&#9F+-xjAOB{o6d$e@H=^xm_CxqjY$Fi%Vaeya{1rdK+{OUI_uXESbW|5e?bX+~7yK_E`l{G(52~<J$d#)@vy&wK`y1kM1h?`RyV@1>1&iX!MPLFXKUf`_caZ1={)A')).decode('utf-8')


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
