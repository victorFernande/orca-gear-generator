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
# MODULE: gear_studio.language_packs
# ===========================================================================

"""Discover data-only offline language packs in source, wheels and standalone bundles.

This module is self-contained so future Studio plugins can use the same format
without importing another plugin. Catalogs never contain executable code.
"""
pass  # [bundled] hoisted __future__ import

import base64
import json
from pathlib import Path
import re
import zlib

_BUNDLED_LANGUAGE_PACKS = json.loads(zlib.decompress(base64.b85decode(b'c-qaqX?Gk&mN))Ya{OYDA0!zI(=+W^&JmVuJYL5#X7HOnsj4g~QB`F<nOVjb56`h=HUoz4X5ZSFHh5vo((VBRra7nU{rtZ}3(5AYc|OAb{_c&)jNDVUO6D96R%I+18FAxoaer~2+0qNQ?0jZR(3p2R_HRx&e&BlDEjzc5ZfST;XUk5Mk8bJOp?kvlP1o+=(P7UI`*Z!l)qskcuJ1HLZnUKx`t-!}n~uL_=R>1gLf`HNZ5yQl-g3n5HocC!h)yQkjvWrJ`>sb#4miQQ+nuAw)7?4W!F#$P3TEc*Rv1`+Z#~wZ4N&Z!^zd_6f7Zj>r(Aok>jk0PKq>zkT*pr|KI}Vz6QV%>g*P?k?XKIf+g7I7qQb!^RLEUFXwBFsFjD-{K4Ih2)RXA<WV=m2k9tjRG1Ke&+xB*w^yr8a+5!JPy5%vajrY-0{>yWl^aGE5pT2q4>!Qo)pyzhyZR;479Pws7e9^YuZiv3T*}--CZS!v#1m1DL>Eo?OG07b_z`|jo=p839DE)ZwM-Pt&SLof28l@VcHG&^olY_BFj%_st)O4)Fj(ZX<|Gn=v7UTuiWOuHOaSxWebN#l5YU&l%k->$Y+r$DKap&g4vBzlDt&u(3ts~YpYtMwWAKf3ou%?`VNF-G@x@Eu9GFt7Ik|R;8U3Pcg3++_l=$5~|_?$KKwB54~yIsr$l{mI<jU3-@{q2P}t>Y8u0hRW4iOxgEN5y&cxXs$-`JSDqN)zjO;XHjVKEfK=Z8t*Cw+8Q6|HtZdwlW2WeHwie-_Z>nR7unr-LiM)kTnz1huD78+CKi!LxXpy9iASxn?ByG9%2FP6Q`(hf7W_v{2w0Siu{XKzaNC2eo8fIJT%^JNCTqw6VfRS#*?R^r=Jpi_UYGTH+07y@6x7h^h0ZA-fhw6oa8U)b0gn(2A43JWKGl=-SVhMn`4ysACb|1Oor2yy}G;adsM`Gk;*39gKH;vJOAzd_w*vr8jVc(#5{bSeJS8cN67&%^xeg+stGR_t)?{S>ISklcz(b;L7Qi*<_olL7@c+WRL=o5puthM$Ha)SQ91a96y>*>C~m_vaL|+LBQsvxZKCpw(~*iJGlT2&%-hO4wolZ`FQ6*BT$;Z&ean6~z;sNF$*V^WP9K=07tmLGJRSTd>TfDtL~XqOY}*-|iaMR@_h_3<F{zwXgPLs60t92biNyvowv(ZK!X}CwL8WaLaq0%o*VNvF);{Od)AlKDiv4c~bNto2=82!scA_fy659=&rnQSG+9w`K%Z?AC6$TS@na*|D2o*Ag(6SLh@XWSD>xk2Ef`CcVdrBBN5pi4nwT;SWZTfEBU_EQ(!Q;FH9xVa?4T=jxuS1*hUmilyqjun^A6zzX&A3g6U(f;J(SQ4GVZe`i%~RF^I|!0=st6Mwi$dPAL{vQ%Fj!ZiJhaBgqJ%0o+`%PgV*EWcCr>!DG@*?JC*(dmw)zyiNt}ZUF+OAI^#H8LyfzP)w~M7~I043!+%ph^^rFMI>+8)zT`7^s9QFU5fBUlaXy0v9En0OfBtN2-%&PZxdek#`K3BeU)e@#nl4I;Baa(I2ixe)QKhXq_O{V?-&cFGob%-`B$;mmcYyQSSFIW#xS-Xj}__Oevehe<z0X;{BSKqOoaGA*P=K;GtZ-c9Qb`xv@ABkzU{W+U|t8$PP@#HC&Mror0$c!e8CRe!WQF=c;bBXkJ<0IsEL;VKnHu-OsZqeVw1W)46qw_xTQENB4p6>MewDY83H(q|26rUdS7?$txFI$tT(okYrH5C<%Znsa&7yFK+BWm$)-X$UynN2{=VA+d*X=D(h)_>pl+wzhjO69knkTFb%-6gqtsMVro*2sUqX>Z*L5^UL6xoy^D&-YHc9mf*wNL5g;Bf;^|LnM#%Yop)1(&wy+DT@W&7{1Wj@AZi<{ypnPL7#Zcezz+`MpgIsdp7D5(U@P)VnM44G4<^|cy#*6?&%}b2X{@=ApdRhz=6F7_gGWYN2hlkot}aqR5b=KAKbMU-0$d-$zziTrVk!Hq^eC$9m3R39k6zhy69sXKr(x~J(5pHJ^z3AF}U4c8>ED4f3KceB3WY9l1gX~SjGBc`m3-2O2{682FtHK;kEmraL+}^FtAT0bN`-NQ}GEbn%2soPSg7S*Khv&Yps#t5mALa)3k}*)h5LSPyfUV)$nG0S7ukLND+t;M5RZDr`MTh$snXup3;t^wX?jIHL3OUXqhHi-eYRra5SD<`iOnhremx5neH}-zd558&oI<(lnyRH8BOk3Zf*0F1|jLtv@5M>17j83u8>*$GQDutfx)%zxad$|;)nWSyt<KymR~dW;2OBC2xnDursuFee1tw;^cYobn{~`-k0+IW5XoT@SD`)Yw%rg6KjxW{0brw^Qr%CQ%uxSn>eKzXIj~R?5O%xG<^*wfl28_vI6f&X_^Rn39486Fx+D?0D~6O4Kq4M>I>b>>gQaPcrrQg97$msDlJD47*Jc)vj!yQ-{35~7Sg_}?Vly-jk#qFSBZkn7=80&YmNKH}qr`HF0raFPSjZs@v+8tDxFlz`Sq}GY`(Pe3PLI|pRN}}QIpWwPT#3eb_O{ArT2c!N$6@e0&+2Vs8RT|cR%4VFc&OVxr8Tt49&NE8QUjH8CMur@VpV&>sIByKS@*0+BW28idLCF0S`%Z`we@fA9Q`eN*B+Y|0-fbaJTwiV<5G22H6}1L4?m9#uFUmq=Bmu$`|UQZsS8z~$H^1(AlV~rch+Ys7q4Yaj5g#`{Vr?QonD(>Koex6@*aDZw58Ascy`)07@C?S%!CE2N6Z%bRx5}W;c1ulPGGkjYmOKN)eh$!YnBy(9uxtKC@FLts?>FeMy*yqaK_nI4~RTGq91d@EytKq^%hd0tOn^_9Z*S!9?rqKp@tnIyiu#i>l;|8YPCRCKGo^qMT!$Pc?XY2G)k%&77_yuoHnfwea0L<t-*YQeyPu3Ql~K+pM#-GFSg}&n=a}7eY@RZ{nI9bWj-y#q@MA8MD7hyOx;ENPy@%n+-QSiaN8dm>$qKF<5t61I3B}JD}36s9vKUnQw0V|ku9u-J=WChZWh$?6w}#`v3XMRtboaF4&?TCim^Z}(=h+<c9OYncPCL-pvVo=#gqP^^fad^10!$7Tom8r$fr?V=cEnG*WOC4d?C+f^dZ9h=r`Hx-runRW8zB@3MhCdts7A@*<cUCvf^dwft>BO*PRR8rjz+xd?~2Y_{i~?=`=K*t9jqas%tD$NmC2hV#oW4%u%20c(4vyES><W9P-X|j8AKk(mbv#*)iHxEq4xTiNVno|FcGR{O$A`zoLBrh5l)<V!Z2=?}^>U9ZWt&Iv|ZJW{a`UM|aRu+`GdTfNk~yu1GULtqzf0g%`t#fLZlfS~45u4Pq;e+^iWh@9~EZ?2ZZCm)~*e%+dXcQv4=qclhYu1CuBjyg`3KF?wS1$U)Mn@O4M04-Q@&oWavwNA@1wyNhe?Ix;v%e;-O|!8@S@S_ifJC#eueg(8v3$Wh!Xw}(gVHmIX%9V_gIXI|CAdLK)7W*y&YJ=3zEMdfE^pZ)7sR-{EIG<Bnz_BC;J^tZ?9I>IS?BHd{_MpTW>c+flHVQqMS7&J*Dng;cENiCtr4ng9#C!FTrMGitDY)vbq!%=r&mq8!qA$MSS#z+bO)7E_V7?(tn@hJ0bB^uR?(;SsZN8Mt=Y+)xQ<U!Bx&}SU*nthC=^P8@C&#pHy7*#5d#ZAh(z8?A4Qr#H4R_k>k2}6=xWaTw6lv&i?Phx}JVUERRBWw>(Hi^wO`yCpd(`s2G^S`nG7h6Z{DuX79a!(h)lj4PjLaLfIq!Fu&?5N>3jkv{bw@utfSO5Q(e$(O>M{F_ssTgdKelA9(qwxE{`_XC9F4iyl%>p<4_r5bLA4AFpu{5#yq!csewWvqsOM@fpB$;fo9zok{DAqz|BvmuYGc6~$WVx_qRIWS=7^*UXA0;iWZL=w@|0E4grf5Gn5<8ip?*7M<tc4J<+sY2mKSf{=qanitfBnakY?OxX*mT?J(Pjw8cJq43B%vieZ28JlczAGStm&X`%NDDr%w&bSDL->;1gSwrqhZ-u%6)iL&8>RcHFn2QHLV9d60VR1ESsjl+l41jxr0yWZy!W2Ri?%FBz54%Vpm$$Dv2w=Z^K?Z_}R!#>4o!bqp=%{eMxFk;QUZdHr^TLuCTSAEv}<`0!<J>lc4}5%B=WUe>VD<h(|<Ugg3)6r+5S^YiG66v?B+#Sx@{~<^Af9OEtlOb^XMsQ}y8~J33EFdKb-9gXy5he1<23-Dj$H%2h_h+V4i+aPY6+TjDs2y=6rW2k&M-M%tztrsj2`XkI5W^E#0`uM_$6I#DvO6FKubQ8KR+dGk6^G_Mn7^Ey#7uM>syI#E8a+;A6hAu>0t?K>wds1`K-X20RcaZ|GomcOe#xPUqy>lLU;?T*1I5`r({Y@{PnYl5_g0G+U2I<oy&J0G496KAVfLyHcL!)DDOWIbYB8KpjY=AM+mLszN;F;cc#@Wa57(I#!PHMr2AKa`~a)0Hh7M|2N<160r%8X!&Jjz>sAnd$eSosI4G9mmQ$;Ip_kStg_fN(<_dT2Ui$8c6#V+H?6lD-Sk{;1*33I5&T0zfD|d?0@%NnC`we2T@Gg0JLm&Y>jN+`S4bJx>hjM3vH-f0lyLU5RNUVOQ<Z4>AZ`(^wg^YJ#tU?Er(8HiUFHvh0`ZPzuzQk-@bDP>#X!M@Q4=E$A=alP$`!k^yqeLOe_q1!?7{4Dte^6HTl?sCxi7cUiyb0`s-Jt)^>Wu4s+?dG$HBb$0><z&8wLR+|J-i=)<2wpMNaX6Hk!Xj9sx{5=(9oZPTpNuI&;HVG{U^X8S)_k90bgKGT5(@sITNk6=%!a)_9*DXup5uX3EE>Ok(`xEw!-Olfnl@k!Eh4g;XUV>WC{_e9oEuLoWtuVm9}E8b~$(Ix*LSG!ADf7Cx&i0GeeESd~xN*zyWTRqyJUex;t>_m$PO0!{|uyG{04fYEe^%(QGKA0Sv>WAudQoMNa#+I|sU45TM#T6cBB2veeeC!6JCP0zc)jg#HjmVLvWh)(VlnjQ4|B)W}&^cPH(QW0u(4htCkP<md^)NvJnZ(_>aDH5T^-z_#{}EfXN!77~P8{)w`B44r4$jczEnCG<>kKYX-!?5q0IlRIYbAq^tybGPsT>9~9XSZb7Eq4YF>wjAS}p>?wz4kanLfe=;CCZaTYn|(DL$Ru%EYZbJGS+3%mnbs4eG<~_PstCqO>ht<&$W8He2A>HRG}V&sIA-6Z915mk?FYy4}dRqjv_4l3%Fi;Cp%lO--QKBX&yz=QH^HUysR>v&u^2J>WKcPx-81ROp|qk^Nfvag#^M$`t{R^{>^3^u+w(kMDVbi<6g#G6FfHevnq`k*yZZ2~@WbE6=3SSKadRs~0z<f1dwe>(9U!H{#=M^&VzQJt3RaJ1}!Jfu#SD<<I<)Jw`jXTQjG+jd|beVnLX_#!NpEX@R<i6hKvwkkJ}7gs)9Z?3_r7v>izz2!!$)5Zt6z`(7xs!23SX;w~6m>o(9icddHWaxS&#JEBE*yDS1}$N|Wd_ekVG7pD{01N-xS_0T^aKW?dW-mw{n?d-?}Drcr-d^WaOxo5uIJPw4hnqtkedETPV`o3_z!MhU^;}e5-{$U&kRJ2?;YlXCOyAJycF()>-r9@Q7ux6cTH^?yN<LSrO`&v;4eK`%6zd8LX<-EqkP$e>rNQ+30f7~Eq9iXEPY}#y(n1MQ$s)(}<(LlHcj$69USkDa`^EAp>it>bzJ^nAKHp)Abq|~o=?)XPV7xT_ZS@dmPGLNLXa-L!q$J12k#L~CN(zgX8Hva{fBir}+EHQ`z2&j4kvpLR2S(A9V@5Ua5hsPhW;*bKkI*lsolTjxbTOgvO2~pCC`@shg-`c)o=ftmQBa+DN^)y?=I~K%Rnq{Xc9FV@_c3U`oZd&vGS>6VwlaaJx(szPL`NKPO?@SK}d|<V=5s!{!MT5gwe5b`{*-fE*b<{wL6HX6JPrn?b?=n5Fa-v|1*OO1q)G^X-np`X2@4SG+3*ME=-8@?0ZGOs~8|Ba6F$S%G=R>@(to-3<!&fI7^nP(S_u;S~(GKSwyz1K3Isq0;#iicnlp~hj^z5^vTbyor$RL%cLk4Mq+HNpk7B9Fx8!wm$!DCTM`djR^G=6NRTYt0OR4I5$i$}L43>6p})Fk_?26wNhP^lu67LRV3<gkl`OI;lZDQ_7xtjapYzQ+9LI(QTRPe)>yzbYJJC583E?}~~y>d52nJ1B}y$a|U>Ws`nV+v#7cTCMYl$|@D-A|-{R9GEuNaQz0+3ezGxXIak*`LuH<u~R;XC|hWYbQ+iRHwVlhjP<>775X;JHx$S2<v-6xCnSFtM&RW>E{!cMEK0=y8b7j;gXT|NI>v{azIfjBJX(J{{U%&OZi^HR-)+v}+iBX=>;}Rx1DZxFVD>W}b-z*lk#>1#|Ngx*dk-CiUJ?DBI?q#o(o@iIn^h40BR_yH{+%DLlYLg{#4jzbj#?`(FOQ%sE-O7BDJ&}WSQZwcReV|y|2;e-cR2l4+B2oan-g6y{CAXw`4tw$tr8)4(QhjE-H>H%$T4{hRm|EVQ9Ei`|6)CJ!fyASXRUu`B*504R@);s;<Xa~9|UIFtTXeJ45#DF0axN@Nf3KML0-&x`U%x>u)6HX;y-c`J?dBKp<Q9ouw1Ug=ru3wKlz|IP%i&@S?EB1!RVIhR!btG$v{yD%Ojec;3;+kE9B!aeN4f^A1)Z^30|jz7@2?l7gCqDvvY-N=^E^@$O+$TxxV=C@87!%LNs$8a-a_Q2w+2P(t!~)I3=Oe61P)Sm>&RC7XG7ye@dc03yY#wDmKdqsxuzxTBNiD{RXrc@Kqw8XIM#mmVM|W!Pc$N!*Mc1`|R1MqxH3lBLiDro5T<m_Uv#z?k-cXv9W~r)=P~*^wRR8XpFq4IRQ4Q2b<zm8u}~X5^dwaK~WRGH1%YtZquQ4T@_njR$722iGHsy7P)?1gwa77oMJ{6|E-?0dZiqCsRvRcuxwgeT6w2CN4%(Mjo45{Z18SyW&bxe)HV8N0?&Qs>ElYVR)k|kgyXSgFs@!UoW5%W4pvmihi+z{RiC7mmk-l@KCGTI*k=WN9`Z5JkYA7+=$Uzx10G2|&^7E?kC?}fe}Fez={kS?iUeneCfCQb`-aDWMi$N!mu=gph@R&~F`?fiM8>06Y+R3Nn7a8Z4>g{CQifJ7Dk*|E=RK_*nNq7-e#Bk&S$+gr_E}y~UiwL1fLZ#<dcbr=HOkQF>8GQBE<jBLu|Q8Irpt^t_wl+92y?5H$9@)<p<V15m4K=S&^L2%73d%-C9~~zIDaZ(H&_iVg8BP4sw<32Tm^i}Q|iPWx26pzZZbkxxo>@uVo?l911A}z<?ChHw0C8KR}()o;jf9Gqg(b9+v}6?=D=9>XW4ZRMI{w6qa}qEQIREuW#OhpC1s(MMJ4&LP4htpN}c$L(x<I3hM%S!L`oizG*Aou-*4K969T>P<J|KGbv3%>!1S)iCJ(}St$EW<YgbAuL;KJ}WZxX09<$5*WJ3i!MidF>x?tTJWMaEbK9wDA|1^HvpW^`X8V<LKhe-1zNd+&Y9|bc?m-NbcT6%hJ9K{&XK2+fK98t@$1o!8?RhZeb(t=BNavqjqZVHRc>w@%O<v8!+vLa-1-qZR4p!wx_w~3^mlt38@3W~r!c~4Ccnf_}Os0_ho;O`zO%wl>gR}6}>52<E+6hBXsDaTwuXTZ7C?TT|{L^O*wG%Z^66Rz_#`xWk?F~hzi%y;~E1`eM1SpX}~d02cG1SsI}{HcIRl6~iGvK;z75=+b{_yVTr1kf~3{~5tJ^mW~_r|gdP4E;bjD~d+p9E|h^w1|Ev19q=wri!_0zbHrl{eni5i}lVt%E!HBpKT5{df2bvuQ-K!c<eqdv6<=F4F;m;KGqkOX%~z6EB`XHBII8F^D^98QArtMt*E3rYOcKe9svG#*)acVv+T3tJ7#jPP0D#Vnz#cm{u|F}0{B_zdIgxP?6Z6fQTACO>?`+iA($!manTh?c~4On(9K<;-+u5(>C*h2y(6dU5}T4c<_e4QuGouzmV;1>%POF#g=MOpKA0~E?#bF}^iTsKNIr{Jha>)R{k9G4F+E1#4Hm!#pMi7j*~qGVAlvZ+>lo+8^qRho&HQCt;mGn_-=!%34iA?!oPNviBPcH8c42N=e1b=!FT@F+41XQf>)ahvRm1FqCk1AjLsqUSb4Q*z`Rw4GXHKzhvQulQd$w<*T^?T=(mpkwc;N<gS91SgK|#swg9QcIyHAt9hYqY7YWF}>Hl4BAQxZNWbWihdowU>f6fDuK)R{e{6jFWqEjnDJzGaqw6W@k!o9ntQ+R@$Qj*Vj(4ibSu_fyZ+*#b1`;AuXLq^)4MspS(kywh5k*2*e%5OP&D@-AXbKZ&lc<$n^_?M8pnQ&Piw3Pa`T+q&XY5bIy99sgMKFeCt}Z=c|$=j&L9(=*20Z_-rE2rwd$t6vjO@~#<6KN$|Hc;ovVA{=f=9S;@4Ikc{eZp;j$8#A*P!lj>39T2T_AG$qj<ex1w9!sx(*IQg9a&Q>`4G*F|cuz*9;#{@h3}bWNQ+nx3VG*ufoCCS<dIE7>yPn|NNRm&YI_%irHf8$@*3o%~E%~C7sLgTe<VkB6slcRGb&V$Jg6dnT%gfW3?&>>tbM81beivOknfJ8%LUQwQ`9+ydbWi5v-C2#=NXR~~6_Lq7SPp^9Y)R|W9ExK-9?Qh1?O-14w@4=9XM+RkQ!@4;lCB`rU&uf(Baz+Ai<$hrp?7L*SXbtaW%{pz+hTGa7TkZ5^Kf*FqvJ>cM~wa+-IByOQDN%A=oa|Btf<LO>zR|=pSAw_tp(p!^7+KG&yZnlyKTfT-c_@8+*w~yDRb*G|4C0@zad^mJdXaR=Wl-ljsi6+`m^*B_RQm=8>`JH)i=SX3((?Yt!B#Y(#B6Ijcyg#nf#f5HFf-(%0FBtZmOC_f6MdZ#`ELR^Ea%6UgV$P(&Q7VlLA?09^tCx*S@q8I7)R0W{pJANW#DC)?EMf&2_3)U;kZn1G)LA^6K%N5(X9r6~N*k3oH(L_TX!;U4|^4sF8`p%S%Ke5;v2B<S8exP6=LoT`5Rx+&<})Wg$^D_@coJIf+R2^liUsW+I6nl%ygd6<}StNTxjYNkumt7v>}3>oiR_nhZyVP@x96gX>+I#rbqzk||g2?(lioxj|-$@u@Jg+}tEf(FKOOvR@}R$&}+`efas5Jl|WMmt^lEtRBB9ZT3pZ)LkScAyL|M2VY}uwpo7PY2Iy864D!*lCEK-6;;|+nU{oiBM}}wFV9ROi-a2@NKNtAk)cEdG1N~{!r4h04W<@c*raYB=MN0LhRSwPm8oQMuK$$7$x7swhf|i_c5(A($5nS@R|qOu5|ni6q%1kYD~IRw!DOG*&069-h5P(%8Ex&nCFxd0nM=sPiYnoD+r^yRCB)ni%|oLu&s;*);;bc|!mK5z*W~S5p1DLV5W?#1IS*kDBkC#&+qZ*!G?`p3f>u?jOVq{CxV6<)_w$!0En%vVD{-3o*EUkg{jS??r&5=Yq<2Vo_yy@p_I6vUxHyGLyDEQ)L90ypjlNTuzJ!Y`S>N*XCAb;qDZ6P`pl<c%u^NfgC3!n2KY@wEqO?4L3C`k;%et}OYiBSKscG=`Tpi|^N7F2GlAFSW=54V!g-N?Og~=(JY$;D8uocKTbFYfM;n_@Ro7s1l%_JsYSth46naO-^G7|<x2uLB7(qw6UDNUxFpx3q+HK`|Ott_vJ9>IoWH)$)1b!chZgKJ&KR+mR<vRqd*HfJ_@bpN4$e|&m<X-#PV;qF*TY;r2TyP8-T@7eWaHi<vT);e2Rb`z&<i^y#{vB*AUIUAVZq>ltAvdnhf3?~>xSdro+S}$9)hDsooD6yl~yi7MV`&wB}iZ*tBK%rVpt3%_%eS@)rRur42?$3wJDolBD%xQa2E}C)8n(0n>b+wsMnC?XLOhbh(&3NJigX@s~Se^7FbUEt@^+VI4#9wae69;D|IFV~qraz(CliMCuB9n$PGTL^>Rq`k6@-~_^F`BMdKmAD%r9WxAfxbY_Ezf^KBHN3U{EF-+TvyD1NRix-EGYV_un_@oI#Cu1eKQz85xl3Pbj-WXffD7080m2i6xHo!r9j!`;bL_t@28-Wo7qmflI^4`*-q5@IVW7CT_B?CcQq4~tvZC{CIMDBk~lWWaq4XjOCw5a(=#`~=H@R^iyBFSKJJUtiA*qo5%EyrBYKWTGlX=?B%~eM1_{PDD?<sZmWl{@Bk5k_p*9N``l-|&*pO5tx-Ao#aHiPflTJgj&g>(0L@OBaP?C=v&doluYwzHVgLj{OL@TgSq4<B+k#{81!!gFJG6{?My^fqCkv?ryn_qX%k-uIz948#%-Hm)B-8vaZsHt`b8niK|{A)$oMzRjCvTP&D(*{+fL>?tC4T;)-&Xj|yPR@~T&733g7erc0an6y+Ze!k)1V~6DT$*tNKjjqIkruPgqFpcVNUEt;6mco0S2GbwvWvDw6d;*Ne0y-MW=@jy7Z8_g6J79Jk({+_<|i=?toS12+DS?Zn%B!zqP1Z5By<Iw=+;P7A|i;&MNh3tQ6lp~Wo{4YvYISZYvw4aHbE<(s)rMH8l<-gRxQg^azRonbX66RIOW$K=?QH{RX|-z!e;MuGLlQkwkIZ<o3|w1S=z}~nztlfvmkMa`oN}Kwp*RJBw4RGaY@u~TYOqh&BP@+Es9f@$PM~-?ZhR6?>mlstX6n3UbE^%CiGXG4hj;QWahgfp-Hk{aYB>4`L2`DB&S7jN|VHV*GOnmZ@w!MoK(+uokS;m-ogru)j+-zh;GSrvc4Q5MkWrqX$SX3dVDWVu>PbR$`Nne25+~;W>uFT)P*-X?EGh)pK97MzOm|tlXz~_kx^t>$x%|RP}0N!Vsv-CZJsXG%vzw89!?Q3r*6*vwYFob?_V}oD!PN8>rlfw7b`<lz#Op)4;}Q?`L%DJZ|IxnJIR~p*LOvOd3Smvb<9!)?n>Q6-Y|_w5#Jl0?x#_b@5fb%5U_U~L$e<rauy!6)Cm{Neaj23-La}C<lf24x-%>^3acmyW^jxTSL0+j$==d)hfX;&#_+P)s3TvA>5zOjG@FvhCeB~OjOY<d^4H*(<g6JoG9q#MJ)$fL>3KA**(Z|CNRk;^EM%9#_YFC;c$W;#MtYj4<5T%bV0^g6Fg8y7qV!(F?KQjvE}97^61ccJgNtI%iXNgAF1l~bgl|Wo0OR*3*@|K^qtVn#t_9~Q`2-rFkN)_RSY(-(V-4>jED1wM<U>gcoAeu)5K_`-$QSTUrInJNO)RkGcD?+Lc~-ZDeIg*+2p6FFV{gRx(DRHaKaNsiit>zfW4Re{_ovJRBa1q}$R=e5Nz37+GuJo;$jK3sb>L!!0v1paXjvZ^rmknmKc6Z*+l%f_&RV$H`_bu7@i^v1jK)fGQG8}nmClQk<*>R`pzI#k=f}~##nZyu{N(LMdr1a#?3^g=DN+|~_-&0y?JOeNtn%d6QfR?0yE6;FZ|IPn)M(qjx6KP0lCiW9T%a34f~oT2y9)S|>3NT*#2P`wCFv>os0iIN31H$vIOl^GM*XUHbFS<26&7HcGzo1vl`p!QWOCLQk=1jQqeq|o5q}EuF0MT2b%c<iH~E=M7tCVqfX&{vZ{PC`D2My3Ll}KDoq(D_+W|S8!0raH(CI+~LFKLEWmo#Dovn{KgcD{jSDo}5^Q3O-hnf!+-1mm?qJ|sxn<_FVevgCW26;(wo|)7hOGR1l66(u|%a)QSqq}Kn*Vr7t!biB~9i>qSoMz1VXga75iXiG_n^8Fhqi7@~wB!MJnM0Lz26o3z{j`|Pgm>Q?5P?g*Osn{D0){Z`%ehqe%TDg3NvtYxImwuG<yoHg$8(3Y(Ens{Ho`~?l>2OKR+xvMcg45{&}FUyfw)shfDb+z1yQNoFFon-<~BZId?>d(%qXq5?$DH?&k6`1aI=jvzOi@4#gRHjIMA&9RHmOr8WndGPnfOfU}zxf#MvIna0wqycWCTQsp%!n<?-R%-Kw+J>WDl$r{f+exg=xYXXPk`$gO}aM2Z<_`U}Q4{sM(*mX|U(<B&PG3rF?Q^WqSh@r}KyQ^7NI2ThNi6t1~(5$#QSv_7u0n@*#T6B*tG>UP^<-db%K3rz?xWaE_-t#!M{4ndq)$&u9fFYZ#ZN827L5uOY{xoK1H<rp~65|bkNX1!W8f}HnGDn=n}1DT$s`sQD_ni3FEWaPLtSyM`A7MNgq!^;|zjGt`ygKHccTHI%EaK&$`be2xM+qnPn`*<N{^d(R65km3%fVS0s1rLdyV}*iQ030zc1R-s)IoIcpx}UjE^jWUb((L4$JAD<qn_yx5k>>kU^dZvNx_ll+AGhER^9Co^3FcTYj^H>>+-vn_DAq|fI$zrnIe2sxAOlJWSy`f{_4+~>p4OxyxeBAR9mQ$+<G&;@dP18aDG|pz@q$Eyk+*`Al3hzW0yp5VO`ZbqTG(A+Jlb9iHQ(H;dX%D(dPP?6$nV~XLYYpf@T9a7axdv_GDddX&KAQuC+E$2@7juNZe?SeF?~iKabuT+hrW8NFu~5Q93KgNi;-z3n_D-I!OP(0)8UC3%)MBe`H*dGw-iFG#d8o<+N?WB4s#fl<jPLIBWAcq46$vnG%sbm4DA*oZ6zROc^~RW)6VT!3<Y-Rz(tmCCzxFWfQ<v(G5|K;j+g{s?<IA@wYy#!0Q=!`0QN4ML@{5l8N;vlit^l1;IcFZd$K)CpJm}haB<NsNgHRULD=wOkq}*^fw(0|Y_l2yFdL{e?<C>aGj^LXRneV-@>4;v`(fxNq1aQT-Gy!jiao8*XPgWa`%%|13-hn7w6{$*$hzpc@pMJk8q$bjxK1t_TR)|p)3kU@1{fP5d^op}Psu{D&GD5WvFTsLxi=r+{z=5w0bvI?*fTKLGvyd;;u&t#Wae%l*fS0GUK2wl;^{h!!1ltsKwvwIiwfbR5!fM)SL#8qgG@4xTm&}v?7L*_1a^H8_B31`s7{N<8e(_7SnNe671rQv1Bo5Nu9$1PHNe=rJ>MObjcXxrr|rzmIchA`NNiaeg~X<pR3fplf*OfU!>j?sw!vIrz>;LCiNa1dDS}`-U7`%BLt?v|1Hhh?p28{wwyI~RVc1SC4m+ydWIj=W#@>wqI)NOmQaN^2%WeqnGYiD#>U`u$0=o>1eSp?HLSvJ>Bat*$fybV4I4Us!CNE?Z_6b)QS{8xrR6wwud<^z9hC>_QaxDm`G90!^sshCJ3USydv3QY-QP>Ox)SI{phmC#1k<%VkAg=7@@0~0LdzY-aD<YNOQwYO`C`Z@Cg*rXE9t2z1IS(i$hjM|~Gh{s#!?4K?baFx1M;tgT7=53`VUuhIGjWqzLmH3GZX23wrv!n$2-Bztg6$MxuxEMzfLMqM<ytu?Y}#U^fES>!r)Vi3;26dc^BYRA*hI`MOcPLSmv}lLjCKZztt4<=AoekuQd?NP8%<g<06Ti`z2L7|q6q-I{eU?O7WCK<wu{TC5Y|@K3Bx|FP}sY6P43yV_mFjD@BZmylSk{|u=ltgs0-EL0pq>Iw}3R9Iw)*WL#@;YrFTjh8rziB(9tSU*y_~9sX}3!9c$7phhZn0uq)9i#$q3lMSDO9sTzoFPRXb>N7Ig(YUnyeVC>|s&WB&`;m+98%m-7fnYl&K>xf}m5IkWy`Z^qZ9M`NwU(YaK<)73}8y1BCY~hu%B_iEC7k*88dIJtt(!oUIF9lyS_L`yBBJfhkYqGu&2SHW(z=nx=SC)e~V2^?@42OMgl9eY9Zrva|3Zfj~7-{D_^&r=3T@)mkmZitM5Iu>!678oLbS=tbJ<zo$SW(s)HwJTUYsfXM0hcN@A^vTISvh{!jgZk=om?;Add3M2thM4){1#`kGOBoi3nE~&wG*SQi8v!lVok9x$ZK$nz-=(}nz|9>HM@&jeX&WKjw^e01EJS}0lkhS%^dL??vKY0hS*kTYziPrL%%QZYuQvyQT^-~f8EFD3ndZ#KO(cFV)tU2a$=gYcEIv*Hw|{J7F*F{0(RY0S72cFHS=~-)W5M%Yt54)mYV=thi+}0^<Fq-K^#4;Dwlz*6{+Q8taV`;Vtwc+|23V$SRW-VX78bc(`k_P-Z~iTq=Fh1i)*JQ%DSMBV-|@s2G57<fmx?iW}~7wiR#0wl~|yqi1)I>S%-E7&N}Jpa}0?bu<y(+fLf<KT4gY6@u4vfDU?4+khN~X5Nj{2f>?V7!rG~XSnH7+x^xM|dOvaLdG=?u>;Q+|)hO#2r0kNAKp10fly%fplt1cVT?p%_xexW)Z+fy%;X<g5u#Wl&I{hH<jE|^BSI;mZiE=E54qi=Qb#BXgm}*gN*)Jf7YPMi2A=N_e^&r(VG8G8rRnrN&uZyTIwk0c&)VmV4R$Umioj_4LN}80zsP`yxQxzos7jC+I2sP0ptM4KLa^TbPu7OJ|A3Ci&Q8n@*)9Pb7>^LjKOY_ST)e7O#s?UJ8MLAAdkI}4~i;yOhh$w_+)n=DgEr4{N;}cq5o-eBwGP=BJJ|;Rfp~Zmc#DtdPp_3C@3WQEgXfXsjGodvQ&=nI}4Sg<eS_XP{n|(RrXh<b?H5-RV_2JL)VVFQ77Y+C`d(YJ=sk;sUbRYm|Qg_YcD!VDjIAtiU4+E_n{!{D6Ku1%hk8JczX+N-A7X}@l+_l<$L~6+wB~N#1W1&Si;WO=!NA>H-Nm7A>PAu77z@QbMhlLQN-2L_O&t43FhQZ$P?i&5<=*EnGj*m2I0iPpRc*C^bHXQe?RbFf^JMJzCea7l-9o5?=p>7Wg{XE@P&aAv0n{v<_J$dF{A3FS5O<s~2R6(F~CJ~*7_7HK<#45D)FAi{qLB}19B)HI4+5h}xb8yh9Gw2aflw%~cQo<t)wBsuXG*6}t7_>03VW(K)aV25UI@m!$pj8MreGG@<xNU&SAjg6}BFestolwIALTe7pEX?4*F$!9!As+<oVbI1w{7|9L+7m16-cEp_72A>76+o#i;W{!-K|;GCwA@VsLc@wSwtFON(p?iBq{YvW0nm>o*-+081pn+5;h$xTZ)<X>ZFEQ<^don{a52z(V;_rXFs>;t69{PB&4O-Km=>{$F30)GM%pawb4nJcJgKoiUPv|RlOIjEPf6eE`%V)1Y_n|ha)Hn3qoLB%v^?-L+of6Pv-~|>nk~mI!9J(;=v?%37W_PU;)HAGfS;4t=lw4J%)vfScDqcYWzc802VZP0<nvKRJkPs;Jl8}#$39yXt5gAf<`34;XMVm|4t%x}u;-en=YUbqh&FR^!>`p=2jPX7=N?$8?T73jbmF5ow*c?#C|{x&I(d+1U89%uhMK@<wR-o8dwx_Z8+~+HxOHLt5-mXW5&#3Vv98y#3t`XZnWK)#4hvw<c%r9DxK9D%`3NFOSY3cSxnsP-h2uZ0Ks;x5RtoccRMA}y=vfsRsAre7D#-aTAN6dyyS)P3vnGpLsAuJOl%rJ8Aiq9)#<70PbHc@*maiL(d~R`&jhE9bykFR76?7u-XVQR(JWTAfsLf78`m_JZawEMDy?Ao)xS6o$MJ9iRdS)7o;@vaxpC;znwv5x-Vc?x3?KU2lhd9E>c^(bS6T~x24yAR7TF?IL4Td}?qhgHsn^{)o%+7?xo3Lk|S|)+vrH)RTt&DpP?R1y8@7&y+y1J*R(Xf}@;UJ*Jd*HQ!Z_R-|do-C{_*wlEMz5~L6vHtFL?5mUZiCU!`y)4@0wTHk065)?I@FbJbfgNSRyP;{Z6YMli;G@7<*0}m#G)fGXgN`{n_^l**bATE3?#H+GEk`weS@M`uYaW%+182pD5)8T4*Vi9(2a(Klo(@hvhP+fXt->WZ<pmNLqY4y6Wq2`zJD0#MHS0of}ra#XD`xt4F)(g1aw~LVuN2+)^EaLNyPh0KtLzH1SVK$mja=W(eF^7GQ>RG@(j-wOUe$Dtgp@!V7}gOOtc)#M#@|A#Y8<&2zclU3~eXD(2B*0LE#P^2_2B_Akp&%9wz9=Xy~e4QKGJFG#Z+L6&edoY96=eKxGoNU6!g!!;0i=mo~W<b@2<rL8tVaAdW}EVkBVDxZe;cX!zQ=x|^%t@JiTX^7`;u+#f7-tajwXp$#o0^9H4e=z~2+g%V{{lDou1=Ud;&cK3*cj%{&ed&gmSxj1OtUs?%*&U#HsA<%JvTrLFK2pr7GIv$ompd$`ZjDi+#LZaqoL80ZyL=<W#gND`&S8HZThUO(LnxR3V#a!^+o?C>0u4^%*anLQl90%R<GdSqoq$Uh5*=|q<gx*n=iF$B_M7gAHPo|<CT<$uU-8?L`k7Qbw6Ivbbl+!<1f`(3kp$Av!zqvN4`Xx!JjY?K$a0StkaG52M(9>PqpbpV!B&SY3)CsElK^he8xnWLzYR0*HgD>+kRPUO1PWYI>0!TCsP?A%_B^|?|qX7-B)W}fHk7-u3DXM855Lns7$emnVv>sqNCK`ce4@9Y{5jx;hfTH=0CMbGOIVgIM-6taE$9wKND>ZE&B}U++_JEUF7b5yG(r}!<FB$d_uY`=$c(B2EXeiFO0fh83oLLR7I8|`yJw6|D$r+AHcG+aGMO{qv)ZhxY)k+*fk>L9uYYwi2aDR6Z1W=uzns$DGEjFq)F$j+Y&fxN#-u5+c(E^JmaSOOiIV>8hh{sf$=BXSLjlY`@*kCg_*-%5R21XaQD?&%pzB8(kO5t{M0Mgtaw761uG}j^>Jpqq)`uS<9rM8MIsmN5V$7iIf4iLU074q=WQ4>Uaws9+T=#;~xi2{tI)h=l)Oaet9>HVHii6oEcx8(<*(m@g_J%y0)pa3R~LfFl@An7U4WMlB>P*`U%LRwR-)$B7mIw(X(2NthzAv*e)2i0S6g%sk!l?rV1Q6D2$394OAN%%l^`{bpkc73_tjQ2r#g6hz*`|vw;bl`l=4Al?VN)*LBJ|7s}_j_%xGg}Oe27W6K8@=1*ug-x+&jWxb$^p~SoRfo#W(54nGE{WvvdOewSoC39l>mHLZk#I5PVMC3q7}h9h6<DmiUw{WH#_y<3h_*Q4sA3)4;CH$s*#==>JR1+@$YKRxX{W)MJHZ;FUV*v1Ty*oa~`m$ZQ}cm&X%W0vMwxoa8_5r5!K|LX=`e57Ig+^YoMb44Ge)X(V@h+If}v7#zg0QPP|nrAkjGz8_kJXIBhbR?TyJ%?e$OiGPas2s%0cqxaj?|Xb*^QvR;B}nvzlLDH02qZkKqKQZ@=O(dLfMM?};5i36IGCvdV4`X?xcMDr5!HGgD5IYp3Y`u-p=>eWg|O@k0b^cBOxD1<~SE*Y!NMVM&M<?I`QLyV7@P;o|Tvfcyw+3fq^Rh*JqiMbRmdK!ZbU`YBF%|=gTLIpNjifG+n`q5M{ac6<igR?Y95L*B}K?N`PR^4ROY~PYHYV$XY^!&lqkTnju5Yj11N3Ar+!0ETEfYGcpio(eCosEM<JCcKf*auq7*|VhRgc$t<Z9Tqb?kTj<>g0Nn(bGf(o!NHesX``dOjz`)&B{g1uV8RA<G=KRk=lF0Y2f@7<d2x$!4ITTda#kM;KCa}#zf<yN7<_zosAkvL9p|f;~|(3>rF#!i!+1Q-ByaJ1N~0X|K`G?2WMlu3KHamOS*s#=G#d#LvksiB}q(;$x_JZn51Y0gr?}x4n$@2H!~wO>ynxpdGRA~w5I-8$B2fi$bUnj(GIh+h&P!WI7Uc=m98TbwTI(<J0g(kJk(BU9%?5i54HX)gONUpFv%=L`rjX)uEI#CwN(Qp?I{*f10`M9%Q4!^>Vnq6m3086(;XhS?j<L+ND5KCoGyFy<_1@~?B#Q;O0;zB4KxYGi5+WJF<?63?y5jc2h3kYHr2sPM=7bjzEcA(?bJ<3t%e;d*cDi5!_S4@YNMqkK@uq{P_5PpmquHthAJWTI?>Wfi6$c8&vX$Yu}-kGO8?t!AzU0kLRLQN<fB&Zv!*_psGEp7+pZp38fve?N)suIVOxonW?5D{`?Q({_5$*BHXk6GrvcB47pE!#b&-)-iIz5uu=-%>!DR^ZDCe{Ym~yl<<`7uv!4=6k{ebq_6{4kiSM<R#dR&^1m{xnow@H!UG32ABGu4Wq)ADJYHWCiCLin`dpH9>)K~P6sx3%l78cD5Qk#3QTryiUoeocmyG&#YZuv(yMoxVyGnxq%3X1eL1tZfmhIy2V=$m*QAt^!x*&2<&XIy=|JQ0x4;u7S6%nCm*Jrh~G!Wq|9!6~GL6%ur4g?iy^NexhmPgiWWPh4L)88~EbYdFeV+P4nc#)veFKS`xa?>}j1SYxc`4kTtwE>%dvZGZdW%VN`4ksFR{#T?wbf`0{X!PW{Xk9UZL;a1ECgI*_sbI`Y9(Wu8tfovP=oGxs#~K(;*ExyJ|Vf?k6zR0dZ^1J2fuy>{9rSS@u_QX78lu)vLt#33Y|cB9kZbZ-Xs8u?&(8}*V3{AOgHhE1E^#-mok-5T}PGB^Jw<etXlne3qic0HP&JBD1-|H%+{h6ubC-og8wU*PBj)G_kf;7nVEHOZq*Ltg9C?h$P^Xxz0@<|EWKyh!jdX?>GyD9%6a4Lkkxj2hTHWWIsCjzTIF_F4^4<(~%7gioz3Iacilu5#rlm)CFs*qV(Q{8$|=Fr$|jw35(k2Obpjz<<bTsM*&Was3qbI-7>tmH;7@h?+ZW1rp=CS&67&mCqYOD=m34ZvaUoMbVI9*ipm|?sby<7=-|A%;z>T(`bZ77yus%hzDZ$S*VrkCQ@wz^ChbLQEekh2I?q4%xJZlIP8Q_&UkKP|GyAz<_uuebk~yb!*}IDvC~NGoD-?Sle;_&Hd(tx2<%b-c3JZ2q;j1Hzjm_l>nR-i`4UVQL9o#~AMd0<*!a^a0%2F=pT;`Pw%wW;sE^JME_e9iC)eK=uuW8k#Kym(F5^(U0)V}rXrj;2Lp>?s<kL<*1bfDzSw*U8SK^IS;%SMCD1~6dn?!;NiKl%>{%RvkUyj|2aM*|XCy-eOtluLw3ecwqq)q`2Te&EEYDgIrHoH6x4{HW~?c96XX@pIfNvDa6Nh8u2Mo7W)2bcO9dR>umnxvTD!BKP(<Qmc2zJ92fO#$qB%IP3EnMBv{aVZWFNbf6$Tc`F>Cc!k5SZ;!8lo(KJ_^%Ly!huE!sI>&KMc(qF{L=F0dVtm{lF04YsYKuyNb7E3)`o9BB|A49VvQkM`OW0{rbDa|zY+tiEh0<w)3QiJYXv#(?w_o-K18*UCDMT=-3>PrX3gGb?p6*abq;4=>5`eKQtlOdbFL#(*EY|AHy&&~Ws2)sqZ6%7bPK5o_xDC)t(C{c%r4!sU3_HJ5e?Ue2?s&IeI=&N)&wy$ymk7-4oB!GI4mRXl*ZTx^Z=n@{VtB1L)7s4>=o3;@z66(6B)w1616JTISn!H5vSFNC1=eTDO4fzXx4+_psgi71C++s#m2!l$&Rd@aiolbT&s|Zj@r)~oO3#IpGYr#5}WK}am`IV8ijM<Sk7+RJ>}qQZ(8DMWgpN4O7E}`YId)8j_maGS=28RY>gqB1IPhdlkmt(IE@u5f>~>pp?FA}k6G^z&e{+ci6}>%Vz)|cMEo$x{)UIP)@)j(n|9S`3c93yOuA?2C`URv<#51ci0FL<U8@gbyfu{N!WT}HVT;pH;p<Tb>OT9jbZ|f*(lUC4V}-tdzv0$6*^Sh=#9K*BA-IDFt+*I#oJ^R0;(h%n<PgVNv!34sZ4MiH4eDwpy>RT2NoJxh+$P1k%SHpQ2WLsti41W$2m$h!=>G)%Y`IFY0|uL=Zmf3&afeNaoG5Bb5za3Lj-6J2;8it3pPY1VYOMxA@zLmP-WB;eks`teZ0*XpZ`f>6Qc^F;*I5d(RY$-&vg&lWWkP+qmu%Hw`m_?RS)FZiw6N|Co2?CYZKvl)`<Y3q2bUX8WtQrxlqbci0B7sCygYEW8MBxJ&Q?}-4mR7ge2T%@*n-Vu&CLR5&w$H^;-XF=vrYb-(&TtPp~fT)prOIDcXLQ_6z`YmvYvU7hGqkQT?Wl&cvTXbJ>~R6YETBuexw|jeZ1cqT%;MBOW?AP+w)xq7sR-&Rt_%v3Ggwbx@uYn?OCT=gv)jksO)2&4~4s11jtqoF#(oQ*UU=YbC9aq?;4q@jYopRMlRDN4tozNJ548p!=7o(`-6*fG}DXpxnTy1eYoYgZKE_7kG-(%FtNlwr-ajB>^)APMimxgu?HW{!ebCFQd^!$H5}EI;IVn+`2$pN?8G2TFxheMB>B1v$ZXu0$F(Qrux!%1=EETMxD1xPpE?gxPuGFUKH`RpG`4Nl5xZ%Hb|1vhT_-3T#5+Iu2H^1B_JS&`Mq|&^LSrA{i-8?$U*BI;(~bqKKx04V(P((Zn+}<j)Sxa3ds1m~yel4u!Gv{l!*Bst7A}Ou6e}Uvk9wrW0P8p^+m*>}kMp#PwS|qgpwL>SKy0-%D4^kzZZ}(n#HJ<0)5+PWb|Dg5ILa6o@nD1SRId_;UDT=og?)$!Ue~ln$j)tNG1y1w$J36mkU|Ld)EK`xU62F6o+4w`X^*J}rSR(++G@c9S-!J+gtTYdgPWvqwV!s}upmV>JsATFYB@wb-F{dEy(W%IbW6L5RGZ^cLb`leg6jRS^f0;L9d@4xCvdt8!k-M}^&wDHKJFUy+RaB@Kk7i0oxyi?i&57ZB4u@X-{2dc4A^}9^)XsjQnQHo7NlA+3fsY<X$y)VsS0xyIBXDxlifAJtlnIONNn&UV&gp<s&>bkj^%0*B74g3Hx{6ChE6pQdq(*9n36*QuBR!&VKWQj2l+tkho{E&k(g-lds9g4Dc_zC=ZN#jiEI*$z28Ra17<A7_odO;lSJY6EC*ARBC_Ro9v-_0j?GUNeC*ajB=$l95?csZ4?7QoO?w9dH<qC$4*PiDAKYv#K$J5PBw^T3h_J1T!!~9p7+i!vU`|k!o_ez1(!Z?5)Hv3Q#h#cN({m8CQO{gVGV;4_z0B16bPR!lU+>#HedKYfGJRy<<iUeSYXGpRd~BwNm`Myl37eqfsrwGfFxb&}$GEND6U|s3Ex}$V1T=qrc|K}!;|y*Zt;&JdGd(P4ra>|Anlwqf6J{FZVy`nxRgS$@Q!{GCGp)-P3ZU2N?VAt3rl-WDLuf`pPcSICxND^rsC6wsUF%9s-<hW#+m)be(}(~aF)N+5{RNUVxtQx%FXm}h%rT3)p6>Ko-aM%rj`alZ%p%M+tyyD!a4}pYMy%xpl^&M?q;b~<tM9hjgNrooI-u*GjW{({TuL%hAE)W(n)RU8dmMNnyBPOj2&<7MPoCq`&<ilu2NAn3ieUxB8a4H5k~F+$fVC2PkalPRJ)d5SCNm+a&tv<Yd4@rYj@ZVp^<t~{Nnl7A*x{lz!c+2~wT~;hw6W1;ck|HI;Uc}1F=nj3PgotAtANc+r$bY#_9aOK90?e7HEK2O4yOwt&2MlKN^qBn@&p?b9j8qKW1|t*Jk~Bi9Ckp>pQiWHT4`MfV-JBK#%O6+#%MPeaviNESgQ+X<<p!#g_zj*PHU0$Zh996J*G))G@>w5Rx>g1!t5B^?=|Mf46@rS?6oG>#B?&1L;&pkA*aTA&-iPD2M1A`1=XR8V?^D9aMIfN>&dS1c+C9D0Cr6`1Hr~W>KL8hn?YgYpHzi%AU6IYZ6*oB-iJSDc0E=F!;ZDosA!ITQ#AqDIqi|#EtqrW+F%6TbzrXzjX6^(spwV$uT2BT@fV%`Tv&m&&T;iomyy@30BD`{VU<9wMJg={zpKJolW{R7tPx5^Im%j|a!hh1#yZl;qVX0XtTBhP5VTdu>V00X#on!MOPpJ^Fx6<q+L&%s4W!=PADkz)*u-?}R&~(RcvXw|ZZy7XthAJfI3oQ3ytp1%I<H|pwDjYh7HN8c)==|N(oi7(<H@mo=F<w4^t4JI-EGnIVH&Do(Iqxt1u!~k8r4Ha3$yRif6cxR=^x1LVI`>OsEF9PcC_h<OQE8t#wKT5qz=uqC&G1FP8JY-upbJgXK~O}q#NZypV@n947(Wk%r%u0xD@g{BQC8Vr`J5dv#!pgEYBMqI&)2WRuA1g*=5Ev-3^I8L%bpKE7ig_mo>}-Hs{P_0jxPOlVyPB{Fy9-GpA>=Bw@5MlhxSe@|mngE|)bdfi3UjBBk<#t`C7o))=<uI)Kaj9XD_UCo-m_9kgW+GHfOs+*GcenwaIp*$_Q_j1*I06=R8-^-;^(@hz#LNqMgiT9$K@Aa!sO=sBu|S3c68cM*N0_#W%F^Bw}4OxH~{OxYA09+5W<>(`>?A8;3Z&u7)48mp{}a#pM+RN2&=@G;zAj2-U*4Wb&O4ADel)=}jPQhYZ6Wz|wuNFOOwL6ns>F1M#guIL4AUBQChSfuhX5<dY65f`zb)Z3WebUc^xEe2{?l)J66lVa6(Sb$~rU`E=i^qSbjyxMK-_Kw+8d^#|ExH9!iO2?wZd&!6W6j0~PGxRhjyW<Zyhy+@8VgiSQR7S5LY&r8(=j3?D3F<upD?c*U>FCq7t%@VbuT8)zr_O*!BGo(sEE_s>gj#M5Zu-o%tVdmEj)WhHz&W@lhm2X?<9mbijuj6w>K#6ShYbdX(efx4RJ^L=vw3OZl;;G3S>1LYoemGNtod5Rn3a<e+eY`Rfkz4TU-wQXG3_$*z<j94W!*7v8w0ki_|9lTKt%KFvpj=AO8;*Y^==AeITiOpb8Px$F~i0yu)k(#?q$G+d>S%ndAGyCQkoq_s#Jcj7<6=g&d2xL#yWi*Ra$ljXTigTE$g5V7UzSD(5qr;s=LM*(~?yknSz4D!9{-o4_M*eEcCJ|pk;|o52(DOj_Z>MoQnD_r#q%CL~*&BFlIC4DTQUuIp;~Ag(Xhs^5D!f$|N-b&HE|<&9P2h1ZY+@aPwJxK=Vv!bL>|HX5K&ehC`W>Smv3YZ_9yC8q9nIN4ax@i?plf$`H*@Ac>X_&vv&SrkS`)d)ri>y;1!Rjmd6H1V$mO`S{qjC&9VELmeo~$#w<!W}bog`F>(eAz}pb0nQR;HnxqU$G`}a?<j>hPfU&N$8j~a8r!zmU!V#-apdMfo5lU>`OPk@hHqM}F4xV1nr%)U9hlJ@K?d5a!xZ_aiD{mlC7npt`<_tEhP#`T=UG=&iIy|pCI;X@cz|(`YBI-;RLohw0^4lQ&f$a-Ko`YlG63f(GF04X@^F+>0&tecxEoM;aiL0v<>=<rrb?lkk85(v!8bo?lnKIllGE;($Y!-<;i+COruk7EXv(&$gK3`RxRD@p^5FQQ*Q_7UY)H`)%K5#KDCVbKe<83tsYb@rO-C@R5D)<|FZOjmmIp~0E2LC12PO5N^fBcEcf;1n<^Y)YKv`cP@(7GHvpXX=4WC!!DV@}-4Kk6#E&eRyIDr^6JM4#pW;S))dP7|#V;h!9q;{Yn9{&czn)k5Xst1#ZWidKJ59n;sn8KJc%o!XCu9*XLjU%x{U;MnyxHle`=~u&N(4SB9`Qvaf&4$&$vzODYgD9oGgU|-;VBnE92RFO$I?(br;PSM(gKx;%90IU;%2q)mJVc^5_V9=4)BSXx(iv&gWZZSlgV+rQIMcLz!&)gsj>DEMbp**qKO&zCRP;H=K@yA5=~z)5+OT2GhTUM(zBGqa?+y7!Nb!F9WkQ=5RNTcj+Ufc5=7qM?>F|;TFi6-FlOBT#70h`*zZR3an^f5aN5at(yks-c&QUO7cPv-Tj9Zg;A!ahi!6$^Vk$E{(6!boH%mdAdQ7rCw0ry9z+)6RE-%k|uzAo&BAaRla={G;P*bcjHP%?s~Lj@DSOVc3(SZgwdy9Z0RA0`e-4Qi!AukIr>`U%kt>Dv?gB=LS8Ki<25X&O(w3g5cehb{s9w`Inmvs;0q2=la`jlxKq8ql26vgeWDIEF`8?5Y~t&_)BLl~0>bFD!Ksy3=};<F_3Ix(#l&^ahUvy4$hzHA;!W{bIn;k9W;bq=Y&Z4}^qBd`vbjb+9t-tp4D%cC|>Xlx#d2JM|muTK5Ya9Vt4gmsILK>Gvs*HvE4;N)_lp_k@xr(c-n|*xHSouyH@)bhqAP4(mx}@!N$#dD<5cw?9ftJK|IzrA-%2DM&hwoy&lvQ-OskkhHRe^D)vUHz~wO?}Hpm)!ZzM^b{-gK6|DXNc?Bsq<Hms9=FR^8j_mg@PN}ZI688S_`=+7Yg;o>-;rGd9Q9LnIga`%JA<QMd*{=&5C8M_)jyOWsee_Dq+U65W#!EEl{2ST&U~BzQ?D$&va<Bk>Th3KS$Zx9Onv)@8!JnfSI)e?a^~#}koxxJ@7LbGmVi;OoOx&E%+;0UA6CwsSvm7k5t@4K%K5cVzRFfM;M70=^wH|IcVjGd^jm<`D@*UKEPc1K^jQ*3z53ntwQFDA{^8}7Ge6vV^N(wvUc2??<pi*LW$8<9`<2wo0IOG)pIce_i&>t6R<E47wsPh}88W>E{Vgx8EG?@ER4{89?%EBS*Pn`U)<56;=+4rcnBk>sD@*ULEWaAVtD{fJg;uAA`9C*bI`%&|&lcdTquy^{`u)n%7q`B;u=eg7w=Z8?{o?&{g!Ss{*Q2)d3M!>1Qoj1_XY#^gxHVNtxBm7s)%x}8(z-VIdgaWUD`#F=S-whiOtsW1FaQ4M?=P;s{sDC#wUCahfY{W*%F_9jrQcE0pMP3jd+RHW#FqBOSnRdS@2!3Rb~zIJ&gbv0-u!m;`_F#<@ilr=6$G2An;Y@gYcJNuV6VRP;?Fmz>F@8n`=_;QpV0E&e(~z+D{tNY;gg?#JVzgQQog4If_>}CpFzmH$?1>V%V*bK{%~dKTovd#u_Sx8)4T3mdVyZ8R<;;?EsIA5)MWK9Z$wQB5!hfuw4rI7M7@{4xO3qTOi#tFCW>1r`p6=%x#HE8rFTFPH)wO5mzqfo_RlwNP`{-BY>O&TA9&95`pL?fn=8vd(f_5x3=sS08y8lW{%mo>QW*B?^Vet#(?BuA?_a(1(I>0lJ+C^=17BM!%fzg1u6_RzwJ8E$-?~cd>)h&#-_xf@oW2Nmy>jNgmE}*swn>~Uf5qQN%<yw!hO6IST3Pz-%JR!e2=>o6UZ!!<fFC@rDKUY=Uj6<pDW~62g&2!1b5o4MCeirwk8gnN4YJK5uVq1Fo}LT3zWw%d)XU29XDiE>WE#pq*Q+nQu=?XC(Q9Rf^HJ93=3Y7TKFweWz<TA(8$6+BSw8+Jh=+w^1=L!&x+#usU-|6L<u{lF&gd?3aM!$n=^el2|GzE^TZqB7R$u<$_Jzy0E`FayVXvH_mtR~tbCG*`OAr3zEF}B(xo_{hc#Z{MLjOpEvaxJGow@z(M|VE>Bo~#v_S&bnzI~s@lm%t4o_l%qFVC&L{oU$sf5#Q_(b=@;j5=9-_MOwO-~R0F)eo-cptB>|Ha|m%I1STYyY@$2H4=$u4WxET6G{TLY15M|sSVUNXAL{!j~~+8>D5$DFa4jJ@8_VkHBx(J>GQRhNUM48u29+uN?&{B!s<oZNI(4i<A<b%(K^+_Xs>?vr?nerS+#nFX9{9|?c#^Tq3YqYEmrW(v3_)U_4!X}VOdxEd}aB|3W#=cqb8KQNZTy|X{UrZ=o|atI`c@{WuHcyIR~*V6q42h%0b(_iLPRba+(!Gw^yIPoYx>1x@|6AIcnRSEuK8R3TJ+}v-Ao{`PFNm6`;2>`#c}Mz4qbh)vsPBF3uCBx-Y_T6TO%#Z^-@>j$10Oe((p<nMe<;gmH`Ya_7wD)i>yCzu+pX=e}Bf>D#r_m-2Aj(Uzy$Mcg(E>Rx;8^6ICTS1-Q3`n$_AtXxPps(tZ35yG7pska~2-dn!&_8U21Zc~~N-=d+cetBc<`dj6Q?zInY#L5B4`8$}BMAXaQ<)XTc`tQjM3A?EVc(1<n0@xKxN9ct-p+tGIWI6C|Q~kumF8yREg+)kjQ8$(K5H*@GZKu1ydn?(iB`tMHZy@F1*4Y<nNhU;7zP|RSA6B3L78*7wrptd~t?-7D7VAKMWAkcBA#Y-P_kGsOepvhX0x=SKm72QYBf#;szkPM}kDsqBy?Xl(=Wcy;n#tuV7{M}em=|C@5c$9sAZEV$#aZS+SBX;ZyifM;C6hQw0^NE3+^rwK;6DC>eSUg*!w}$imTs)Q{0Hv(ye5N>$qb}nC3ncR)r((17$!DAJetjef#3S`bBKAQ{Xt{A^}!cpf3o64iufzC+Ok(@qdj7=S^GsqeHNM8r(ZE>&}6g`J?^kbc{PbrK5;W};d{2z`#}}77lnjRFXfE!^ipDYv{o$KS=@Y<OD*>d6c;W}49Mhp^k!vVv-bpiiutp(<9~kq!>=qdM({b@hcZq}5aY%({(N%_+_*#Y@Y98S(6~vH`Ka+!jTkn5`|OvipZ=IYjjvt5y!PDdNzgcn6H?u(AmgU$Ow`Avm=f)|k}0Tx9WU<a_Js@9v1~sj*ztruPbTO4QqR=9C2zO%S_vRe@K@S^Z=PR!>9?BLz(s`KN&w}#-cGo#*hiS{DhFL|dhnpg|0y9A6WH>USft^T@=zcd6FBpfXp9?19+N!8IaRy$!Jpw+Jo5>*rqXdgr-oER4YL4&9<^Ql@Dj{Q`L?fhvkVR$Yz_X7mu3}36u{6i^bbF0@eU84xc8_T%C%3Y7><7DV^Uy=!JLcQHOy88h;)qY`7^AP{&ai!Y}A%3D3@e0E}dJy1b@!!Z<973znRMQ92No8#nY#JnCyl_Np33xot|tpA+46BRS7g5P7hK?d4sVMdxlhNK3$+czAXc*<EdDpRWSA2UtfUL`ptE5X-2bBjaD}$N6PB0K&!KU@<qy6q{c_1sVoGo^BKt(tG~OsvUGj*FVB_3)s;8$gFjPE(}GDu)k#hITo}dLw_mR;y_H3(N3K2E5?Qc%R2ntU!>o(DkA`CKhb&%QYO#;{Eu&%qXgzWRCcDi8tVdO4kVfrX)OzHYTYc^QWc5<`y6K@yvch82y4fZ>J!y1#Vj3rMrg0)~8YhaTaUyRTCvvB8qF@>)@~3g4U>YaNr*WcS8YfDoaiU-vRhtsDx}2{>O2pcY5AK{kPcpPVQvJ?H@7+0nU8<zc`=ACa|JTZykF=V9?)GO(q|DvE{E}L?dhm5Dqh=HFS=`GvN#&BEt_!&i$G_m#|MtS~>*Ll_r%cgI)xxW1&zvCie;`BXEI+?0hdI@N^<T?*4#dgInLn_e{3Rcf#(GFKT%F9vwGYqdE?Hf?x>QIVP|)7^`G<GGX0_YB0<^yR)$6N&c*Q*Ag$a<<ZPo!{j}D>JUFez-qpksD7dL|?F3#B3CPtv?=ifjq``Xv9(dfCK^e3Q0NWS>YUHNXLYkEjqid0%tBbO64(Q}6cZnvPCEd5T?l5zBXdO5rIvo^JG5Bjh>AHT5npBIv@{g>!P@>N4bzr)1*_UpB;mr0qij#;3`<Z*vA)993pWA0Uk1$V&jF#4id9}Xg3)u$mb8&hYX%t@Bdq9$ueH$?Zj^<Tf`_bZ0=#eb>k94;b$?Sns&UM~!jR-H`T+n>EHc9-x^xJ+LDMqFxSKd3`{n%+pOSMQAoV2Fr#X3x*bNI-VnHP7f}>Ctd1U%GwqMH0#E`}zFN=|A53=KWjm6Ty70j@g!fzxvV(Yj6EAcIylS7EhEH1s!mG9_^(lKml|9E-k@tg~eJdHxkyWP{FWZ@P=%oNqRy2{j%kWIKiTcmx&m{d!s!juf|wG3EG8#*GF_PbXdHKIms1qGV=60pcK-&FB9bw=Q=OOeM+**;D-p5zxC&@c)p(#w`9b{bezab(mPEox(6de|1zyI;?*Uxm%fy^2Z`rcIrDNXm(}bK3p<|>(6sZ&rX>C$ioB>5v`uA`6^Qsq>*R4n1hWb7`D(YZd0xRU%saFwa2ONQzVrTTux5>e4EZ*Vs22y)+Lv#p;Plz!w)F92(b=SFNSns9397$+;iFqum+}$yru1L^>3Nd=#n}2HD<KDG|MQL0Yws<uE`7Lm?UO9re)R>Sjq@hne)a6jciy|0MBCrKd|Dzr(_njcDybuRS|=&cwqO!(kL|VmGRaqoVUhwJ4OfJ@SFUY|Wkh@^t>u@*v)4ZOsT6om)t|K1-oA#DSjZREpa5|%lYmeFW3Jd1`wn~-Fa0htQUiZa^=aOz?dt32<Zq%Ki3*5bTLHqiBosm7Rv?Goe&x>FXNzF?i6fsgZ>=m};dmUG8?;?ndOZ)8Z|Y{Nzde@$<flBqQYC`r^KSejvvjKP`No0sIi%ymtB92O=6#&CF(Iv<d-v8W|EUih-Vm-8?cp4Re)1sf)zvRv{rUSBvd-%)V4tV(0u$Nih~!8gsKspyK>W9_UW5Aemz((iXG^3PV;T5-B-=+JuD@(Ur!oGDu=61PagiYWS#^0U1@e!a=n{6Ai}c4b!*@XZ^pcp!bpZd#Gozn>{E6fav1omMBr3sA{FU#p5gX6_UET$dRyU%PFQbKQ-FvwgVD*dht1o|t(;Bmp@pMz~1&AV#=+)>4$J&4TnD!CknILsY_Pj=Nl<MiThF4i(kDi~0b$)t@^`2KnCNY(Mh9hy~m~!~n2CSa{{?^6U;J4?vD*B?F0AcLQ56{wE(>IEWpg!%bufS$Md52Xu8UO2iVEz_9MCAR3-x?5^40Q&JL8-%+<=-m>tze`ZcyT~(uof*fS(4%>P`ydK9n%nv`o;%rfxH*f4KXs%&Fe)&9?FFRnu@O`&s|@Nx|C7tgKzr(OH_09b>X$=+4q$6M=bwdSW(euZ2ZLohWY!dbb0%m=i_f+<BYyRd}Wt-$T9zqzT@`W^c~Nweti)VjWt4=mDP{`%uD(z+-nG}i?{0rUreA*mFZ2!;Xghi?n3CDzK!iTHIgW5g7)U=S5{y8G!v+jvj!V@V}T0M!~rW}d{&?TdiBTe60wss<)@e8z&M!POIMVfj-xX#MH4&B8w|8GeiiX$Aefj5(_B}-L$spo*`l$d^Jn~*b*n)fPJ8ADkx0p}|7YvYM}Lr&l{m}Q(-#x3rxoQ0U$uOh_scwqywrRmb3|MzPB!z}gWTxcl)!`odmRGv!_VbRy^=VFcKbm#xEFGXG~REn<1{?CV_}x!I!x~4S6457y|Vl|@0*wp-mi-gG9UK&&p*C*`;TuWnKe!O8wH;_@sLnyEIyW>6FrBha`k0ep-ZNpuxRn_=amSe6lZsqA;4uXl3*0^_c>f>U%ieGz?qTay2k6H{kr-*!Y@<65o}q-#p`H*8+CJnw8!vc7xK~<tLMJH^WOJa;cV_vEMh&4aHB6z5HJ&lsn6sMJ?bK>AU8SO^=;-jXC#>M)+gWJzIrZVBMD6<qw8ir;umwtLfXAd2I`G-62zB0jr!6USVWJex(OtahzqzxZWijDOP6kaaAWO@9G!=D0|yc6qq<GKhvDZNpD{Z5d~}FlzD)LJTIEZ;Dp%`EM)qBfRBz~ir=PE*0^Z$)4Q99E_Q7~n8`HxeQsiFlZ7|&%$#~cj$B!`@4LLZQ3>nW{<51$_!xt1?>yQm@&0OxF;(-e;cM#s4f44)#<q9u$F!<nA3GCghYaJv$F_I`}URzoI9y3O~`Ab=a&)Ae=|A*GB&B5qM0AbH+H?K=y8s5bZYo|Zu35}uZ>0Y%xTxLOn;Yg>lzpKs3XP<rc{|B`>dq4')).decode('utf-8'))
_PACK_CODE = re.compile(r"^[a-z]{2,8}(?:-[a-z0-9]{1,8})*$")
_PACK_PLACEHOLDER = re.compile(r"\{[A-Za-z_]\w*\}")
_PACK_HTML_TAG = re.compile(r"<\s*/?\s*[A-Za-z][^>]*>")
_PACK_MAX_BYTES = 2 * 1024 * 1024


def canonical_language_code(value: object) -> str:
    """BCP-47-style matching, accepting the host's underscore and encoding suffix."""
    return str(value or "").strip().lower().replace("_", "-").split(".", 1)[0].split("@", 1)[0]


def validate_language_pack(raw: object, filename: str = "catalog.json") -> dict:
    if not isinstance(raw, dict) or type(raw.get("schema_version")) is not int or raw["schema_version"] != 1:
        raise ValueError("Language pack requires schema_version 1: " + filename)
    if not isinstance(raw.get("code"), str):
        raise ValueError("Language code must be text: " + filename)
    code = canonical_language_code(raw["code"])
    if not _PACK_CODE.fullmatch(code):
        raise ValueError("Invalid language code: " + filename)
    name = raw.get("native_name")
    if (not isinstance(name, str) or not 1 <= len(name.strip()) <= 80
            or _PACK_HTML_TAG.search(name) or any(ord(char) < 32 for char in name)):
        raise ValueError("Invalid native language name: " + filename)
    direction = raw.get("direction", "ltr")
    if direction not in ("ltr", "rtl"):
        raise ValueError("Invalid text direction: " + filename)
    order = raw.get("order", 1000)
    if not isinstance(order, int) or isinstance(order, bool):
        raise ValueError("Invalid language order: " + filename)
    translations = raw.get("translations", {})
    if not isinstance(translations, dict):
        raise ValueError("Translations must be an object: " + filename)
    checked = {}
    for english, translated in translations.items():
        if not isinstance(english, str) or not english.strip() or not isinstance(translated, str) or not translated.strip():
            raise ValueError("Translations must contain nonempty text: " + filename)
        if _PACK_HTML_TAG.search(translated):
            raise ValueError("Translations are plain text, not HTML: " + filename)
        if sorted(_PACK_PLACEHOLDER.findall(english)) != sorted(_PACK_PLACEHOLDER.findall(translated)):
            raise ValueError("Translation placeholders differ: " + filename)
        checked[english] = translated
    return {"schema_version": 1, "code": code, "native_name": name.strip(),
            "direction": direction, "order": order, "translations": checked}


def _language_json_object(pairs: list) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON object key: " + str(key))
        result[key] = value
    return result


def read_language_pack_files(folder: Path, strict: bool = False) -> tuple[dict, list[str]]:
    """Read only immediate JSON files; invalid optional packs cannot disable the UI."""
    found, errors = {}, []
    if not folder.is_dir():
        return found, errors
    for path in sorted(folder.glob("*.json")):
        try:
            path.resolve().relative_to(folder.resolve())
            if path.stat().st_size > _PACK_MAX_BYTES:
                raise ValueError("Language pack exceeds size limit: " + path.name)
            raw = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_language_json_object)
            pack = validate_language_pack(raw, path.name)
            if pack["code"] in found:
                raise ValueError("Duplicate language code: " + path.name)
            found[pack["code"]] = pack
        except (OSError, ValueError, TypeError, UnicodeError) as exc:
            if strict:
                raise ValueError("Invalid language pack " + path.name + ": " + str(exc)) from exc
            errors.append(path.name + ": " + type(exc).__name__)
    return found, errors


def load_language_packs(folder: str | Path | None = None, *, embedded: dict | None = None,
                        strict: bool = False) -> tuple[dict, tuple[str, ...]]:
    """Bundle data first, then optional local JSON overrides, sorted by metadata."""
    packs, errors = {}, []
    for filename, raw in (embedded if embedded is not None else _BUNDLED_LANGUAGE_PACKS).items():
        try:
            pack = validate_language_pack(raw, str(filename))
            if pack["code"] in packs:
                raise ValueError("Duplicate embedded language code: " + str(filename))
            packs[pack["code"]] = pack
        except (ValueError, TypeError) as exc:
            if strict:
                raise
            errors.append(str(filename) + ": " + type(exc).__name__)
    directory = Path(folder) if folder is not None else Path(__file__).resolve().parent / "locales"
    files, issues = read_language_pack_files(directory, strict=strict)
    errors.extend(issues)
    for code, pack in files.items():
        if code in packs:
            pack = {**pack, "translations": {**packs[code]["translations"], **pack["translations"]}}
        packs[code] = pack
    packs.setdefault("en", {"schema_version": 1, "code": "en", "native_name": "English",
                            "direction": "ltr", "order": 1, "translations": {}})
    return dict(sorted(packs.items(), key=lambda item: (item[1]["order"], item[0]))), tuple(errors)


def resolve_language(value: object, available: object, default: str = "pt") -> str:
    code = canonical_language_code(value)
    if not code:
        return default if default in available else "en"
    candidate = code
    while candidate:
        if candidate in available:
            return candidate
        candidate = candidate.rsplit("-", 1)[0] if "-" in candidate else ""
    return "en"


def language_pack_payload(packs: dict) -> list[dict]:
    """Metadata is used by the UI directly; there is no second locale allowlist."""
    return [{"code": code, "native_name": pack["native_name"], "direction": pack["direction"]}
            for code, pack in packs.items()]

# ===========================================================================
# MODULE: gear_studio.locale_catalog
# ===========================================================================

"""Adapt discovered, independently packaged offline language catalogs to the Gear UI."""
pass  # [bundled] hoisted __future__ import
import re
pass  # [bundled] resolved intra-package import

LANGUAGE_PACKS, LANGUAGE_PACK_ERRORS = load_language_packs()
SUPPORTED_LANGUAGES = tuple(LANGUAGE_PACKS)
LANGUAGE_NAMES = tuple(pack["native_name"] for pack in LANGUAGE_PACKS.values())
TRANSLATION_CATALOG = {code: pack["translations"] for code, pack in LANGUAGE_PACKS.items()}
LANGUAGE_METADATA = language_pack_payload(LANGUAGE_PACKS)


def normalize_language(value: object, default: str = "pt") -> str:
    return resolve_language(value, LANGUAGE_PACKS, default)


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
_STUDIO_UI_HTML_TEMPLATE = _gear_ui_zlib.decompress(_gear_ui_b64.b85decode(b'c-ri}YmXzzks$b8zrve?X^@pkCK=4k%F3!r4J#j2DdlUD>@IZ|3fv$WOhy&SU`GV=QLS1?eTx~~VrTDg5=OIw1Lib)3#|qaRx^#g8O#CmLHS+xANm)}PdGF4N4R@L@R3#3(qh$8B}spno12@Po12@PKl*6zbhq`{**+V@qv6hX9^nTYy5oz-g?9V!<gj(vIBFj?PM)^g1=jOJJ$di&oKoG`Eyn|I<ms8MXZy$dkc}`sw+A01FLqgX;D(VGKQ2t;etE0F)?~)m#rl`NcQpyZxWKx>IQGU+@XGJSgU3DZ((ig@`mxIVu^;>HupD*Wq4&5}sd7NE9}m5q)3EEZr=A<KW<2fr!J{>v{+&lre1o6cVGzWt-+7@U-gCp(g_rEh?=V&_cP`5AWU|fvsJ2nNU+X-Si4%A14KcarRGm$g+;zhqq&n-)R=sMZmIuM57h+zgUah+-&mT{wF#_7GZPj`zS@ymh2iUsfIQQ$dbZ#f0y0u!pwxx0hQ@|m-=(t6vzRH}<RaS@3YGrGyB+3L~&kM`Zv;)L|`t@3UbG>Hf#bGeMfV}nkdS^qR8++GrdF1+INcX(H)4#8$Ph$`J{=jwDJL_6T&mTeZX7B#}ErDYI!%}v;T^LlzsaD;s2b-xJMX+kM(|0%0`BBi1ML(;ntoEP=e>OL;qqU7vx;XDxc7=6GnG4_*CqZq!|DfA{pl4}~-hTk~H-Ng%`U9iYD0bs%R1RJf^4+bCx{-e6hDgAE9~hx(<a9$nrko9D!x1?Hw-;QAW~*##at+PFAK44>|4MyRG#<J=A3#Mw^UcY%kv4+id0?dtVT@~zOza0pS9ct3vr9KD3Iby4Dl0U-i@;-_92Qm?&WWK{j&7pZ8?CY@Lx24G*zGpy_W>0@4}dp=RrX0|I*zBS455}IFZBB*t*uco4z^ig*M;fZ^If(Z^gMvS8;ql1=tkJ;!7-F6pL-Y6p&LRTR*5EV*L(P#x8E^m?$Ey&#ObN)_4>8`W@_s8=|6kw_BZ<X`<?8m>$zTE10<)e1<0DZy{=dHx_MK#yV<Mux>-|q12{AJQ>{Fx<;>pRIyAA7J$pNwU8mbm&)!-GBuY19_5$a5oBh=6z5ifqBV&#dgKs^!-<dUg??2e=%$>dU`|!shF;#OGnY~(t^^NS=>uhY+y-v>T#rh9m-a7RSqfveG);1q>*Eh2!Z*Tp6KYQ}_9@MMO#sZVKMnk*G)@lCMswLv*d&In*;JO_7Z+sj>F{F@$Ku2zPfg?z5PuyOQ%2cT?F4(J3zIQ`FXn};;U9J8x79MywJCffxKK)^Ewao^8ujh?1t>boIUxdMQ+>-);Pa>jCHy8$?OjpcASu~gX?#LhB$O1}~Bn6;H9!i^vkT)PTys|>8Qm55n8X^CBL$3>o<6!I&DX+ZFYd;o1N3doOsNe1w*M8rPydF_tds~)_x?wOJc3|b#NFfBGY?6My&8k$6L!bm73XLR?ItI}b0(<3F985=@R7F8ceR2|6L<*P1Ae<k}zz6|v)2zw?uT2-uOPy&P2V+!`Ku&=KCZbYhW4!$F0K{@^4U?8C241BA=t@NT6mYmV91_T$A5DfXfa?!EqB4Gh^a!C%KLCyeDAN&f*-XX+;A{8TGtd*EqfcP`?yafT20S&hIbef}aoLCU2MCEY@Ip*}HH~7we^VAZ<Tj(FqulZ0E06R1g*(BvIcumH1-zlw#mrejtB5{`AkX6fWMvI%!s6xktWhU%T~d^Z1|ck(Vj{nRwWQ}=Z!?F_<VpuPtyjiICrfpgIwRKjkv}dAQX5c*!9}3Y3dfoj^0&pD_tV6{2@I@xfkgm?Vy(W>^Db7U%EqdHyeby}8eQuBokuRo5)7#=ylIk>2qpQ8q8CPz#BY}JR~MpJkOy}k<uJHfp6>Vg?3I9MtC38%D?#4-eBIC`V!g5<B%&9`$Sc63T&_z|c{PA0DcwV<con)6-W0BD9A%p2d6GvcD;mEp!l)Jp@M22AEEyA~&MBM{_F9spz$T}_jP*oHi2H&rBzS!;M+8z-o3!o-DPa?0yB~C?5s@R9#>lA2YNA8P6`qv|FcS{O#J44!Kc<yy5ti7r#0paBLFV*&@L-0pK`nI2vCE(?s(7i@xHf~qP~EteGNisPWMr1&Kn)}ruqgPG$d61)_JUZKJNHeob3c<T8+?tJx!Q4EGgGu;^L*8SvdBNt^3z)IU>4|3JiZHS%n)sQi;8PDa=9jJN-i<KXY$%Seb1WC22)A7)t!bB0+|H9?4dE26#_Vu*Q3?c?8Y>z(GS8ABviMe8S)SZgzHG#;~*|>!??JeA#i=ZTue52r99bS>usVPWT;Cot09H3P#K4A?0r^*@klDm3S2^=ypL~C-mg14*#LIg9m13n`Yl#1`@l9-&ESt@@qr?IUZgsmw_c}3pj^6fZ<j3HCUFdHIK3#p)lpe&P!`5d3>aaVf&3x}OH$$HY`#KG#Yzh-9)elY6DUhwz0EdXn0U=xrc}{oxZVVkHFBteAH!s4&x7za%`)~h1VN(d;#Vr?OCcO#-b=Mp%JizC@Ld21l5y|}0%bJ8c~R#3f(REF+#5r6Sagc@Em&<pMeD;T*EcrvRvsKh0Km2JW%nT|Oy?;2S<O@HLr?OMkj`R5Ge-c6+EiMvj^Gxl&8zb*;@nY?$d`dM?lcaJ1x73`OVBRaXmD=X3t+!|9P~VP;$Hd}E|zC4w-XW1^dPq!<1b@~ltT8NH(07)$WVfJ2;ueorCg#|mTS63OheGFzr#XoiOgKv!s6;%wX!us!_HWJ5frH<y4Inu$*|t=g_jsqCyQo%n4ufYQYtKf6~2W2zKP#F6lZT3U=r*?FC+FbYkET0)Z`^nV73<W9ye#BUdf){%EYnkB;S&X1=o~7nf?$4m`$S<YwK)oRkC)|#DbdIHJwa67@)|@-c<_)dj=OTze7;Scii4Z8u@BI@_E)%Jn1mU(UFSY65GejX*73k<f_=&Q^xA}+?n#HQy<ogGuT>3>^!)liGmyLe8UTIDI&4W<mNOH=}7x85M;7jx7NbM5N7ShH`6u?#UEKR^}}z#5=+gjMc`dzyA#dW@-Ml)*XXWWrx(~p&6s}%*o9Y#(qhJ)Jcaix^dc{g5>0nP3FW>&MDcNV&J+N;1Ak)f+qCIy@}ILX|2;750^c^zy)`=btqhbHm8gun2y;N@>@PxZ;<<6rS(ST?D&Jp}Y`Y5@z0{$^{Vj9vk)c0JeczD-E*M8G`IA6Sz|aGnfJRF%F`F4Cq0Mj0B$TM)^Xxep)*IW#V@oRB?GPtvRGWFub!VfE)_}pPb5u&LokbQ`jRBIwKxspDOq-|toj$&J=Tj054RWgbGGifBYot~fP3URmW#%qph8_RCEHMf<;8Pp52bIlST~5iZ_l!o*8>(GmGPPlM3z8<LsZE|AVr+HckeqB-XKuCZxx8))_pJSL;w-Y|@P9DNHq)Y9^HRt=12E6ybEf-yU`&gSGbg)^cGijzxtCs9z?3KcDI0?>;B!!x;+#g$+~!jfO3$7f4ZIl!9SfIAF!9D&YJ*iYIlP;px8CtwFK2ta%;Da8wxS};{9Ju%dKV)kWsjSInpb|@9q=8ncQNZI`*(6&>1b9VwQeJ#8Rj2*9F~$B)|$PMGo!QT{qMj&lx+#hKXDN>TTb`OI4dyWlrNkdP`Z!T3}wCvi~>Ss7kV8ALo~|lP2C}Tf?HH>m+8jgyzOSbQKYVR{0If4!-utrU?W4fBTU@p6s*l(|BSKU;A8)eOr7hHK)7DIL)sB7f7m+9LJI>}9*u1K$}GdlJOhlF2Wp1a>=`<1M!uVQWl3qhlr<(zsX4w5G-%`LNY_>6q05I7&+FEX#z|<eZx2X)dbsRh*X9`b-X?v1cTW+5G#&eKp3yIjM$hN#kv0o!YPw6`y2M}4@|atG3$KjxA7nAz$oBoIRq9KuJ#Vd!zw@{dL0-f+6POyXs$F=6mlY}$@wMSg&9T&-OkiDc$6c+Fth5~0#f@cMdQzsaR2MVoGp9qE*C_qgwx4(HX5HGQ)Zd4Xj^sf{@u23&XS(gx_<39Ew!^w%jJOEhj;*`sJ|ng0&eYTPCfex&-8CxK_>B*)Z?uAoi=nCY($}Ru2^Z82)TvBN4VQUqi&&e4i&AG8bYE*@U0=7xdMj@wwwg?~E{Pk92DhpMHR>lm*4dkAe+)aL{H@Po&eTh~AZ<k{47ayC9t^u&N5!ZV3J-G;m$S#F=(=?B>?igB-BK`rT4@s{m)XrO=!3M~9eCZ>ut8g4=`on^PreLDgJ@aqP(LW*dM6f8Sa!;N4>tOthxZ)v?S8gT!24dv?k5Y`vO9v!WGB2!lNt6NSO8|$9&5%fC}JzD>5o{8HgZ82lXv?HbM`=Z1o5DJ>_r211lwef<cGQ_1P$HAvqhhOi+Q@piyql-HkT7L#$0&i`YfY%jtfd{tD0U5aS%XJRqkG0KkR}Gbz@|GR^L$0UDl;4-S5k~QKk8QW%lBaE{5f<JHB+IMXtywiYs9m2UC#gt{}L*R`Z4Et=7u6?mnQE>Hxbbvc^F`S3Hy((F~*F16_v9blWjcq!!q7X}-R&zIBU81y*K`vq2M8yQNU8D%>xIZWQHD*uk`?Ea$y2n25tPr06s(ZVABe)#*XkAcPGuxrS9zh^J5E)|1Kq;g3`#VLp@{=Pu6b;=oc;XF+$L#m-&?%x~w25F2wx$`+hGouoV2U1yX&b+TqgcN#B;fjB65U>p=U>v`+ZvZsX)W}}*IUYh9&k#nq)&(eH(g!S+MM$u!R!on4V<S<26e)jB>J-+l!aDHfxk@E#&Ht|x|y0+fI5o#lcfQTwNEPVi7e?bqT_vZeT3>0-soW3Zh8pBXF+Y!k)qua_u{cWn9N|4q^<@V31!k;aENq8&wh%0zq$^?v8ce6p$@mUS;^V9Cqspi5)7}?PAglY!#<Z#Y$<{i#S>M!l#Q0s^IPnS-~y#Rzb^5W3%E~ibt)vK0Yrw?E^W*fQ8`j>Yw+}`Q%nfAtm5M~%i;qh23WXl?a>$z?g83y6ZP!x{7lBum<p2>HvTa?kIihGR;bk3TZ#oD!X8=bORKsO$E)sDI{6_4Br6u9ulz3c<k1=gP|8L-G9>s@cQy|poiO;qG}gez(K1eO<q4XrC}Ct~5)GI#FTTA^btBc@?RT%z#1VNix`-*hNk;??f&V|Ik2w&x9Fx9uiZo&6D)<a|rxhKuip7bW1`{pmN~efi8f*}*>F{l;yEb|!(|@dCB-+(Q@~;lyNo7ey@lFu7LW&>Moyb%y>`&tLVIc6pI4p_qMNaySc@Y`d@4^9^UlLC;c0T}F52oYO?HH%T0KGR~de*LmV>FP;y0FEjg4h4=bB_|#>2ayM_r-2v?LfGE98Th<v}%|g*O#NXOgEoE+bu(_}sT)vQ*b10T=uFAa9rQwM;tcLC+5*Ia9hy-PR=Vi6P6lM`UMvG#ZMQ(sBA)P<O$wIcA=AF&HoUyocc!!G?n{%Qeyn<c7JM?Jblt<r7DJ~lshtgXMAMPa@*Sf?1DRn<@^5^@vZFYFrq<J!Di<3CL%M&YyJN8E|=X@Z~*>o6r7)>eyeWj1V^E@C3)Ev99moH|s2rE(TZaQ1eRyHka_kj*us|=$pRpoh^4J}(sGYnTSxPS86yXlAS$cvJG5EF*Mh<%xLJO|r2>pT(vm$4^<a&O6=z*r6>Cj%6YM&=F=<52;?WX5n?aN-fOl<Az$y+6_+-Nkk-u4(%2#W(;t&=vO_{4qNxGYdbh;I}oQP&wifHgC4SH(SJd*7h-5fq2)gL$13_c7Nw+6IAQNTtY}rcd3!CjIs2g&ctk~r@4DBVI~mRzFxvbTUiLG<{fMUwL7dih^Ze%Q!gqH{V2YZ|KEDXO%bP>cT+^QNUKi1lAkpIi<=#E>sU3z>VSrtthI;iWwWgg3G$0u(Q5TPQ$vnLO=|>~Lmy=CLIySA?LMy|-MHorK_->QLG0xZ#;o1dLOyW|T6@w_JW_*RC5FI%Ri$<VeO}+N2C*kQ0HxdG_5*%42~&nrzRbG?{9X+TcRDN2ji>`NDh#rgxWxL5E3b5?FhdK@P(l|uJ6t}vnHeD^9hofc>8)!K>!KssfytcGhq{De>iW7b2|u9afweM1@4QWhC_m(gI^?B2{n(2l)S>Q|%<AtFKZire3!<~Jq0{Zkl|c)=Yi?A7`YChMVy1O<_0RVCXaz1TB_{!p8w3|kN}P=`ChG?1MD^?Y*IrLQ29$SzxY!WhKiR%BWyme*w86E9dp#IFSb}BB-X)BClrW)r9=5<e!cnhu_uym;+qV}E9XIcc-(+b)6WokhEX^-Ms}sEk4<1;K5D%)CSHkxx8AxNlq6l7FVz{cMG*B-LgZ#_W=|zm9R9p;$jyu$)y|vxt-1+!D{s(Qa-P7Z<#%_x>5BK)Vd#AhKXUC^|`>gnHNWUHhJq)7`_!a(535&na=5bnKh}#!-Q=rJ}A^TQyOWDyG(-h0AnH6kNu2D6qv*%ULjGMHKdYuP2<tQemVYy~pHO+JAT-xF^3l+;p%y0p#SLaYD*FIPiH?$V0m}jutoYS`Ma<Dq9lyEGWU1pkl5pf0zIYE*nXNXa)&V(VOQLWA_VMm-w7KWKNi1{Ehw9i!kXLf&vJX40CYydn(((rKs=W1kNx4LA_KO&2`2sd!I%23DmqNVu22FO9&sUxcDoqA%`rqyc%do&o|yMmyjfk_yEe(1duQMe+fGyFS&6O_3Vk(0W2r&9`sPN=&AnZ<iclO+{&L$`b=YX8Z|!$%y7ngUg;l4?qI(jj#-tn+Ay&0Z_>0|!>CN#H<74;(0WyJ(Dkv?ktsd9)^8p`l3m8WoZkYfzg}@7dUs8*29aOV&lt*T)4t5ISTr_UNN>nYB*O*t7k{-u^i&mnl^o5t+4kB2|MT8dNR*x5&-P$4K4<Mw-myg8kNwss}Zr%L}fkJTBDk7sRT_zoYi>B)EQDK$Et!4*xIU{%!cUfFn|1=*0ONz{73|?;h`>QYur+0;W@`sU+MsciqY30&NqF<X5m8k?9F?fSz#t?gADMDjNmXy%Ar+$Ax;uDXbZ#CvH4oy~l-PD8lNMjmuhPlfKvLl?U_#645VdfZs7u{n)6~8T=d8Dm4cGj%!Y36RifDNlLwPpNf=a%4TJq7m+CzIvVmwPsF{pDUf$6^*rQj_vs~sOKKFpKd9Wl6ez*3O+vVK?7$vH{n9}JH(y>T&R7H1$Y&E7(cIt&(3Z?n#72dTCzG(KR+Fo~KJ)>;m6b|dkkBk88TgZ~T;V>ifMR3ljW3XCwyMB<?r;iuXVBXI_yYI~bjNX2U~cHU+#~gIfp9r<{g9ndGi&+1Mx=BZqi`}4#e`{aw<+v!bLe+ra-Q*G@JW(4k6v0l>%vZoK2*}igtobbou?k`^!zS6*gIyw`A6nB)!U!(KO0px8ev+svOXG_K(&sFuPJ$9#<)&I27dyA&_SyQ%)CGm1wA2TJYhwYPoM-V?#AJ8<?|9g^TjPJJKy}-|MO^#L(2mmdh>vvdkXkxCh&ip3mjN982N9!R13J}w?}H{U;pMm{zLZ2kVyAyTVsOI=5Px;jiKkpw_k@g!_V(Dtc&w{jYXi7|C|CQuJ|G_d}vMFeAU63bKwXIO<|5G*hvB{ZjTGe(pw|Dj<od1NT|fH)Jk5D5Rus(N*d)(6S8f&meazqbJm(iJ35D(-PE2NzGiFeh>q%ZzWJ+vF=48i!Pj&zq^UtGaAK8cHJ&u(Dm-@8lu_F)lf+!=sSuuWZ5F6ob;+BE+cD+icZr^$vl=9~h4vr>9mYxttls1|qC*#2wGCb*@9g{6LBu|GN0WzaciIV}J2fISY`YPWyhG>6w_oEy^4&TibxXSenZ6^U@#(-Ht-<gmBYfOAJYn_n?&;Ad$0zLh>G}7YXN}!`In-!VwA3x7Ps&k6Fh~0bEyjUtv$OO4=6<WmR@l@1#yM-9H%^+zht1~U=?SFmebP7r)$X+Q43xXWr_WlDb_P1*>B$-ue{#BaxG#B)rZ+#H5m+RFs^zXFQ@2ZkI_qK$QLR<jvDY2AV>%mC@e1AH&<k%=v&M3$@B9iDIWW&u#B?lVv{$2qwGt-5T8)8(ey0W!F~9v=z#JLU6wH~jLEJS>VkBh?ekpsToRbbai6L3sVJX;>A3+N&3p*>U=?*X5&=y%KJ;NZb73?XYua$0f)zqN$!iFN1iVu~mN^OG94wAR)4T2#E!N-M@VB|4aYkBQTrJ|`#+4KgX+xNrKOoDS0ev0Js-du{p!Rx}#UC3(0-HbFP&I-p_$nKITu1DQ8M0D4Mt&fX}poT9bwlQs|74&S8IlloNax|HSZ6CKj7I@4k?3{bC8?7CVd+*W)Y&KB@q?(ZFJJ0Y-;P>3&yEPMn4tvp|jbN&&ByVRwn)u^^%RYUV)<S$S((gv?te(kCAYjnB{TjUk)(-smUE0H!=2GoY;?A)*jqbv;+(2S+tVrCkD(kAelJHK2-w+T6B-VlnzshhluUTV^5hgxnEzg5JB<+auMZRu^`c~z>(eRGy%<X>;giiA8_LsQZ%3K80-iiDILFtF(vtTqz8HJr1Lx+}XH4ViktJymhiVn8t!H^<>07XPfYS)R>pDko$#5hC1&<>c3YMS#pi7s?Gz=}=yURsEWMN8=>vSh)<-9^EScCv-RMUE`!dF;&due}-bNKZlT=X|cm1}|2B^J{!%7ys7j`#OAQ-~8yOtXA$0u^^tvi<lH%#E`hGyu(EIKPnk>L@<N3U!ju)>)=hCyWufEX%807^a&#(z*$A?8KXkD8N?fQhBQ*wZHjkY*tz`*_Ey6HsV621JHP$;#P0=J6DB=nyneq-05hk}Z~vhU1<;q{H^0uDfVO-yyDB5Jr@LzMP!hXabe1rpgvW(yVFy}gMVtURtiK$<+6Ksj4eZdn!>R*z_3Hb9wGMa@w>G^IYff?F<mF7k9I_Kge)WjY^Xs;Yi$J^QU8L3%V-0{o61c!_Az6?T@i(VqnQ|=w2o2DVTxVrWZ}a4xV-)v$UIdE)D?Y8UbJ)W_b=c9O<82Bdy<OThrJCh?DQb1s9S?$-H+#gJJufXt_MEjthzrdpZq5<8?x>7LmjwmQW{#jS*Z_npRI9|O1myF8Q3ZwgtP0jvAi8oVWnSDcL|JNoees<Z0Bno)zxnfj#}3DrUPyLUSSWDJ*4S<k1~6uy*Vs3I_EYw`Q(AD<_`MsRQP7*h1Rag?$L3vyDKsG^Uj@X~h{4BQ<&_R=gTvZ*cUTU`%XuGoIUFzNec)B+c-8apT4*+*QXfr2ZxK;!RP4hBy-l{+Z1z}We^9URIJW$j-7`AJlR<5Z2QJ3bVAt%2?A(JwqfrUA3*s<?H3xn_p0#7p51qf=Ed#dP=7*AKiI1nSZ1ive8OI)W3ww3@Gw2rdXpwzG3=6<ebZC&N2o2a{wqBt_mu0sQIrDZN7fSNtj_`58j{?*5Ica0k&SCQuc6PlGr6Nr0>g~@KQrhRV27}nKo1?UyCj4cvqn<`_0BYg=jrY^w0EW_TkkW8;1B%KFg9<%#a(b9E1jc-F@$8{D9ksgwD7Esio`=2#d6qT9QZTwh5&QC8fP~QZHlCS#@w<SD{Ykq!a7TSFoCoIjZ3&dZLWR7%^JWNlbL|L474XWGcqI(I+h5>>XpCdO{K**l(VfPucwNfb67f(*qAeq6VG1q78rvPbF7w?awJ)r#6ydNF;D$=XI$X<uqIXXZgqS`cmJCi<F1G%d+dIN8F^g)KSqeMX-+c9B=Jh?$+JkMj0vo+59x6lfS61?ZYaOiyd_dY4wFOr?tD1Ai#csU<s$$QZz%0ktY?}iY`n}4YO*`=S-0Q+R>_rqu0~QW%4E)Uc0cn+JI)e>BiNWT8J2MoYI;9zlpFC6h7FRuaUUx7J1LzMO)d>?>V|e?kOFy`~acj1MkA6>dCdc;@g_)Z^p~gd%wkW>y&0qf~rMkl|t9Ts5q5o!%87tK|?n(;T8$PW~Dn%{wEdp%kpuJ1K=a!Z*Eb&7+ME1$)-e>Hrak8If7a|-HKRl&V)LG72bbkSB(Ypvp5aeDvCc|XQpOB#lISBSpc<@VHpJypboDJZs=pHT%9$ENo<`=#Q8L}>z(5a?y-Wl5lLBf#x0HEcAuq!rizXstD0B*eYT(H7@%!Vtx$98>K1BNiKk3el&7-kP7l55!y2x^ZXn=?Rnj}=e$j~hTwVCx`U9N}It?cjbO13G};n@)zH(Jl;a;9aKyVIt7<I(9Ez^rU&_T?3wHc)w<GJYRb^SME(3xJchQccTkptKETniAL(Z!;?JVwlB#7%UE!2a9+<JMaxdH3@v1arGyWG?~c3}6sw$#`Mmmxo;VwT)x}<a=t_38!1mgh2iwO<-hMC-s2soyubX9wHly3Tm0A1M#Q@CfU<R+GWVk#YfV~Qca8qzwOQ0D^I-5)8YpY8b?{OD}Yd1O&__Sfg@XsM^zl(rxjx1hQNlmG#f)%j!l$yGhS$|mtHAh9w9I<RZCFDLVlR^^<Ozk-UxZ&abuqf9`fA6?7B(!k%9lYY6XRzrXif?Oxb;pI}@5Az{z~T3nT_t|+hhwvqE#5{s0v=pg-AXOsc-ClaCIDKS4j@|rD1^n8&u1tDDQNuGUmBoD-+AIj9xHzSxVj|JK_*DF0F7{?1OGpA$<roRZOPOvX3l0#-glD-62|*mwzTc(yUK+Hr~6Q~h*O^SlBm!fLp?IA!d7Y$EVWC}Al`ACK*lH&Qxdy8eTPs247>jAFBVtmue^?wZE47miQON$LcX~@mldCToyAq<q}T01F!Zt-;pu!6&*ZMei;&!E7r%_|oGqKME17~RTen2A!~?(k8bdEEr(BADe%NK(qHDVgo4R=UscM5+K*`UYwsTDgd*_Fr?w@eC;HS<qb_8zdSdOCKniYYpbJ>OjXF)>(`3U{NjPM6D!nbTjNcipp8WG5M;?5?7r1r7~1nQhHA1omFsi8ZV6sVaGY)~NF?ru)dtG{n!g7XJs0&LKT34T9K2?=T+k~!~gMo`s1gb~5{gAu{x(cfDWf`Q%p;Z*C`Y_qy$o|w(N1yvWJ1a;p$YUf}7=0E;7adAu=JOKXr=d5`9SB_J0Zhv;4+-$O)t#Z`AKNvPXjA4W1%R8Ah3<w{_sNwvNX4D{-{ewy4cVp5Z;xB5@Anv`3IfE+>nZ}H}Yz%T|*1MWAGJ(8TLq_ILBcz15rYyrs;Pl?zKWXist83AlRd#UJ#FyKi?>~8Z<giZ<_n)7gp5q1R<HOza({l6h_>-eX3%x9!G|t7drg&4je7xU$#*R)uIor>@7_CRJ%e)e;#g)_VM2l$XIOgibO(YoqX1f!?B2qrWP*I;kbFeM%;bpq!fWq>eUV0($MwE6DN-)r$=`_89Oy5ZPxTN7m1Buwn$Ays>4Lnn7Tu#~|mAlp?(NKCprjtu%dv-$<Bq_8T5~-jF{N;aT$6iGDv<^q))O`D&-=Vp_AGcrovE80bh6aD}ckKIqjP13&DAw*Z<u@s{AB@h&A9gBaqoLZ9#h|^P{udh7fjhofu#G-GOBfYq4rJ0ZUKob#=lGuC?Js~6>w62fbOn-UURS8h&Nu(zXRwA02W}d2rqdj9IgjX1&r8`aEmDXZx8n~nAS%AMXfV8s>Wqd~@(QDT>NVFL&Ughe(<M&7v@`9sMZBS1H@tAA<D2N{EDvw%-Mxa|zW!VxUOqqley$5$ekb^4-CT7hdCP9LCZoTZSFrouMfCu8_OQZYytGki-t9gF*X<QDpkEet*0(aR!p^<V_g?yf!mtH%%o}%ocgPOnMY__DbGowWR5sYj@2oF)F_&JYW(VOy{RngV;b0iA-(5f4!p{C^GQAF1<C=QoF4P-0r#IC~b-~W$-;gH(!Cx;VUuCs5*IzWW&_2PdutjLQGy|^j;-BUgZ6s%ilbuJtENnaks1!ym+Vvk*tKF@QIw}|b&Nu(-|GmDEbAfhg!2N!wUafM#>l@$v=qDTR5p=yLL4SM^Kg@=lQWI$ru$Pr5v}@-2(=KSIp{wH0%uty`u-wAJ>I76sUygx9emmyO3!@3Dj+gGziV8utEer@*Gcf3(nM!wSp&th0IMoJE-8sMyGUoED-FIw5L}#(u5Rq&s+Sr1+f*4e;E_}{*VL6J*BJvg69r}|A?(gws%2{J9f*ogT2ui-d7M_Z_*S@J?$+xE!3yZk@^0@;Q3#>&pJiv2}ea3dDF*_T&cslsa|M?Ye{z0SsJcGN<U^`vvVt1M>KNOsv@5ZEIF~rrZfB{AEwmJsdd0eQ$L}K`q9$v$do9U`$dbE0*YKyEJ<LO9sl}Bn@N86nC6ry;f0rZ!CKch!><Q^d4z#aBAD+Yh?uduUG{o`Ct$YKkA(7nHRxZ7y$@1=KkAG4#wPxqn3QLE8z@aR~y3&bs7!Xk$C$9~SVkj+Tq3D8{iQoZIm=WYX*!(INo;6=$}l=s)IFnJH?4zpl7;ISJ#9CfE?Eo@@&uoAG`|MpKjX|X#Gh*ZxHXI`gHq9~c{zWW@nNAErdh4DH2=Fk4$C2q@Uq|+WTopoJBJVOdn<m@<e4YER4;h;@Mi_WE*noDvjRWVMgm`t^Fj4ER~*^SAUKQo4uo)^U+F;IT#OEk+<%d`iN+EF*egFG3^<G26x%~wBOkeYO-cv;z0-_!`2FP*XoYPL6nr0d))mLEA}fw`Iv^B^S^rywCy<{c^53OnW6!htwuL8?|9fCYcw2Q&h<@}7V}A6Ihwxb&5|dD3(d*6s1vs0%xdzKb@RHP)Df!L>i~7>_Gi{OwQO()QeSmLwj+D!bX-EEtU58>l_Z;_foue-<3>RH_<_S2Z4|j2Vk?79um)e3P>|zc`tBH#|$U6MQpfo;B)Pz*#KT?zuu!W2&WP*XibGC%eziPfrd%ho$=2;nQd3y|craW>;;~q`jD-P}bA37is;m+uW5}dn9(A8HkEXL(sqe%}@V=9Ze@L_Mzu7T^SeVp(7PoN|`HXnTj|juV@c~xBexD*7Kv;`|O=>{`&u#wP)740r1)cuds87X7hvn^V@%avU`Z$U!Ws>+Bn`nX`O=F)Y{)|HTF)kH_}TPs^+Of*<8p8@+JsIB6dh^!R!7r;oJu}mHY1w$*F7>cHqxENGeb<e-Tx@_mVO5gd(+nJ;7_h7-WVQMFyj{sX>wZ%YRuQ&Y%4=#qHVyuU2IH<b*;mS&-5AH`l9LIR4Eo{q*8a2RG*wmR6qIV4U%T!xo5yqkT};clR-}?ZGEUM{Mt~@$}@h**e^9vh#g$lyiE%+h`sg?(Uzn{U1=;VxeqB)Td=**%Ees%vu3V9`ubv1N9-TBds9(V(QI|RwC<s%b`kCvpWaD5G~i(3of1n()>E~q7&LU4Mgh=;E)#}CRP6Wrrixj6K@>RlXHt!^M>AJ;Ev-qzO$oZPApiN?@rr2KZ?npG3fVkMO&~osR=+vq*Qx6S~x1^Zh&W01L!H9YQWmyk3A2A4g$*{59tpZ=W|UjDfO+gjoz*iJKJ99W-n;`q2dJ(KW=~0Iy^pIcKefl3)$!lX1B3N_@bnXP7>$t8;k>hj=mzQ3!e=8<I7-(&klMs7c%vV@{A)F^$7B8i#UIM*hKer+nYqF&r%@LOD~MvA^YurZ~yl1=h?%1mu0A`X^s4eVqEJsw(elpf9FngP-E-{ozUkh5x0<IU;bgizI0N3sow3}=$-p=f!;BkTUr>aiMsLig59|Iy%>^V09>UM(gsDSS)c=0%|`!0rM{85*;qV8;gYkrk0<i`<F4ypd#j8VGWlWv$koy9&oRF8?{?ne5$PVRF}Ht<=ZZ|7mM%bJ?VMDSm`+F+rSbdh#V{0#0z1C_)wsfAnnjCrVi;yj*V_8;pc64(5#qW{)4lx_`kc+U9HjLDD%xGZojg1F%|CwYod_o*2ZM*lE)OOpda}ko^@f!N`a<<nf(N>jZDjmlQ<q*9f{mtf*-;NGxTuQ$ZYOPUIVkK%r<+-kzAfTny^OU9!vr7sm!Vhswz=iX9S-sB3ODq6uq|m$FF@Jsxr<C(UNt3v*f0nt(YM}@ix`hhBXrPjd80|d_M><acE^f#AO3B9on2r!v2_Pcbl-MgI_MyG`{U4a+1MrDwFUZtl~S{|=G^{lbL$<KT&0lvQ8e|U@(>m))s&vLvtVG)eR^AmwcPN+i(y-%J@q2qC&Pev<z0NK<6;`}N5=E_I^wbOZvWz2-RkgW+mqK9IDNW7?4f=nq%GGm4gmGM?api=nRD-TQ5SN7TTB!NLB()M^TwCH8^ZkHxo)_fy$Lg2$OUx;sKp$}Em!P`>xUrHCoT-7<q-<d+n7xfh&8DU-qbup2ZDf2*2rbkANlzgOYO$!%5*yz4{y>fiMVc!32Z|n721u55?cs5dNF6i=JDGEWD(_=l!t}jqW37MOKHzi1Wj(GSstaV*!1E6UDj6^-STj-PXYcszy0OK)TOhGg>je;hwW(U$6g8p%%YvltLd0RRgNY@Xc@){Ms0;Xbvth8$3c|SRF=E^3}IuioasZQ$AHw4#DsRjOh)TxLF9J<C)XHo=4qqEBEfkP>jon>!j?ynh|&jT@Can^Dw_~fMhuIxKF;kB%8Xcl8VSolkCfiZ;%BhQbv5gloC22CGcL#HNdW0+F@W(a)7xL$;~*Tl!-qMcM@iE1*rVmft7!z})&y4aiWMuafAgcCY+|oTMHtaN4;Pv2=}j2;y=<LjiCb`)kx4mvi-#s%@)lgi4Y&oa5$MNK&(VXJoa>vgiF|#-8r*Pvz@PNi&Z5L4-vT$|<#63tY@Q#W;eX(T(m{;ZLXkY~wPE<Ad%Jxexbv@n^VdJhSZ%VNgd|uJ&^})sh__wgFdt}dhNd2wOrPUvj4h@xJsfEt&!+lmbx|x{^-&+s%Kndk$wnS0I~Ca%s~M}*j}HWv3%Hx*wj0GmZ1*Ssdw#oABx$$VI$Ek-?e#|kfdCedcAs80OWtnngg(9s3)7QKsJv0y*%6js%{@=$jFvh{!5{c?VDii$N_9Ym?FHS}24fo>J&T)J`f2;@XC)V7ZrgKcYjVx#dZ%{V)6qp_-VAuZ+;2StIiKs7=XlP_*^i1Y&cB>7=Rvt6H)e64_DZSbIw?5S;vNTX;sl+@Ydw)aSjEl!^06xa5*Z;FqIRN!gFlM8p+5n&qS&8~x%4ga7ufO5GklTT2krDBayaxairJIX(^mVe@!8R7V~;&%?KU0+wlUOAyV?3=@9?xuCBD}@J!!Wes%l54yN#p$Ce+XYRE7a;S-eOq*Eo6lN#kioN%4>@l~uU%^%>Y0-<d6v7FH4uz;k$^dj*i1F&_W$eD=d1vO=L$fuvCpK7ym*$_sZv_k&;21jth?R0^dR)t8mfqn8qkYwfj*RaPh$N)HLN-)F^-0CI_iUOWxQtS~_uVHW6gtm}?@J}`m@Ekh{@^iK#VF9tfs&|^haQX<V^D<V{)VC1QhDPBV{+2nPli}L01<Ht#R582z2!YN4=kae`w_liI64yT}$6tR2kyIKzE55?-LmISO8W0>vh(>|3iv2CCwZ{RKcl?3s|l#Gc;l94-}x<mOGFd#4nbvPMyIk>wN$>OjF1@^GLad1ULB*w44S;9+%Zak>)x0tO=fwDuxgw0|&aLAMGo_nx~gXVbitFRjMy%1EgB!4ozQMuUJB<IqnNA@1Ga&1-ND*!g}W8B4lRk7(fyn%sA^_iHx3A+vWSpmKLF!n}8?&`#E8OyhlOE8c?bx`zJu?=JXRuO7%|EY6M6OX8Hb_jdX+E%qvO=t<(4itkTlz~x&c+sRt>-lLLsy@b7SJ=HI9}29kAxpid|2Vu_1s_@p#6z^OJkWhr)&xCt1lxReBIYnRQWR^|>K|h<ymSW2?tn#9urj$ReE|G8K|XC99qw@<*81#>gwG599v@75`8pnbO&+g%`OvEVZ2#!+2kmE#lRaLadpbZZx&)dk{^az0Uu%t`S3zMOZ3@1~$Wi!J#(5$XuJJ>};YmR~-{0MDHrvg^JpmW5EI@e?$$)<wr0X4_FUbDM;mOlBK7=hOK$p{@j&{);`(xh=PeE%Q9=G=n0T*-y=dik0ShWiusnXnkq}^(qKgIWyv9x9HfSS5d0)8e|1o&ZW{qc9Q4S%UEUEgcA_x2AOpB&+;a^5(`rnuPUEY`*|U%cVXYO9ot2kju>v`e-Z-WW(gnS=rEt)K*F6-ri*I?<z(JT3hU5M)+muJu^kHmh4%_-q+8BKV0ijQ4>6U)7ZP(8)GE48wD*=S#L(wc>2>tkk0<m{}L~QcsOwW_43Ehx=gT35RWvep65O+k6s&YG!6RT9)S6f~hruWZHj)>Nq?%&rJo(tV;^yd825JTRta5K!Gta;I>+*>5($X7nA_JWt_ZiZSv}Q+Ex8+wjtq)Og-oqb=#5IR;Vt_+)#C`SXmm=sl23OEy=?;M8MA=R)Dqo?lAK790SwZx>-$yFETnI!iHqS6q$Hg42VM_$;>eu+)RN@`k*1B$sw3^G!MDJ68Uy4h`h>4FotcmnU`-59@lviQIKMcx|78iLcHg)#n!v9#b!QR)Mv8A`W@IJ5n$gETR6@Pwy0M&^4TJ_V10NF*)ll<{pG`nJ_X5xUd0q)v_5i4rXM^&hP@Ofa<?l^cRXQ<<f0d~Zd&xzCaLFnlieZc7sa6SO71j-qK^Bt3c!Zl4}FbDnfCiPRJO!*cpVsQH%F6$Vc^ENogy9jQ~VqTt8Cy)=(vkPjt}~18mC<fC>}s17xu`o0h5WSY3sjXa(I1z?Dh0S*sV!)d20`~4PGA>@ssJO<AsQizCq)u6+b!v$sNNss+0*vB#{z4a<7Zn5&pv;7YF_->*tc;aQr_F5%{JHg%^UzAV?fMfv)M~ScD7;nM;XDR_QTyA}MTl3i}LO*C!k(|G91SFAFMX^+K}s=Cq7}mQW_sKJZZ6q(>YIPB|J)@w=w~xIvfW<Y%CD80%$#Bl)P;sp>!Q9*PDIpM6VyCa?)e#;!b}h&^_@g8+BV1~a?EA@saAYZ%{=grbFtFH8ziiS57^TJ<AZq7TXvgim-q33@lh(7nRXRalTmWTZ4LLmfQrd#o~%kf{wqg)4pfRExqc)RMs2#~(966q&+@rt=C<b&)G&Iw%Nljmc)|3reCu3;YG%Rl-qz-&|$RdbO0HRH)&@nkrq?)_&Xj&QiV_qDgrLR4bsvHj;691N{wDgVGE&CJVY=LI-cAmub_2FV7|oq!b|wyp=D2r&0lDfb48&sHe0j3$m3jAg5AEUuWypG~`^It$Y)*j<aLqY-n&oC?iBIT|m=PO1WB|g_o7DK{8TN+k|aw)xt|t5i{VbTn(z022@;STRKQvx72!TW(k01VkuJ#HRh6*V}jr*X^Tr~mi}sWIbFnTV;(_MDsT>blZ8^LL{?+Mru1inCRVNhn@Y{LDwXmTZwq_7fM_S3T&p-1Tjc2NhJ4K|lkSV2SBJK?N((9fR$pe6&1uq-sVMPi?D=w-Ui`d%pF*8@&(L7hKvUA5cTvPW!zj`h@Q-*BE_Pzs5(ys}tCm=ygk4!KeHUmsSIodGR+JfRRhq$4)>KU&MG&MoV99hl^5`O=pJ>Ihk*#tY8JTT3^UhER$mARq>AXf)0PvI{wc=+l_2x34wZv=7yE=F}fk8xy@ruX^V@lC9C#Wpbg|?)fsBl2I0FDKyqJ#?L*P~jc<d|j)sgR{$<XAVQeN#0clQqkxG4-{f?&&{L<1GPcwoq$Is2l{P{it$Y*Jg8;?bHI6E`m_AQfuo7zizBcw)NFsnQYGMrIQjiG@)|CtwF;iBZ0(!r4A7kFw59$A!y_xP%FV9mCVtxvyH?SL^B&f+9_mHMY~Y~Gi6@3fLi$oHI-DY)T&%vN>;hFY1&@r>=Fn%Ba!QOfcb_3o?+UyfTv0z@Qg&f9L3eKgveQ@@kB#OXA_}QsoF%ajp?arU>4w$z)mZ3ZM0h1s^)=q=7DxHKs(u>4P(Bo_a}J>(D=y-il-L}RMr821u<O&0cWM+MuKpyCk^DEAz01i6~xB!^JJGa?w)ZXVNajDk~ER>Gs`s^le$jG)ES4>mX(h!q>}h-+At)wI3P*y#EFF{ml%h>mGspnuM+0T#YR<7wp0skk&flnSH2(Bv9#>2hHy6WBpfXv>u@vS9@B1X05<Z7OU#6<b5K)|WY~HwSz?z^;>6Cdwa5=}<nL72Ve^zZwfpyLY>mEe)Y&0k^PR>X857yZ7+L{ub_UZ>p7$4hQKUUWd*g>W@>d$7Z0ulMbcZl$&)uG79Ve?N%qcCu%;fj9$_W5L$MOynxR7F5LQ@u5Sp-x%{*^s?jMFPm3m>`H4a5MQO)49S`vzcE^U4nrHzdL{QN1N_tYsVQy3(Pf+X>@hoxDN>UeaFYiZ;72o<*2eYz5a+DA%QbYbatw;kO`3BTqFUYbtxP?7?cf1LUtFQC%_fOC{YLXhL<bi_rO+vzpZk6_vI7LCA_o9-q8*;NuaiJMg)(VpAoS;1vfbY6u<QLrZ5Yc>+E;=DLlO0Jt64e|WGHgP}z{>m}9+J@>T<E_MjoJr?T#AeGmGl`5+i#xOxgGr(mHK$w|h?>cTkuEY-u>%e)wWH?^x9x>KKwJ5?+CPjB1D+Vm7G2p|*Nd%*&3K%eCVS<xMAw({RM1~1iF}7vJme=;Z7A(DkmNXMIVhqzeg%Ma~VP}<1BL9g#Bg5PYr*gxN%H%FnA^bx)#zrlO8ahLkY4K6~NWa1k3{oh0k=Nt$MAmcxOc6nqj4g4}Y!Tb#tY%8D++(ViKj9QO3C3p>DYFL~$(C4q!gH_B2^01?aaQrh9#m?Y`{hX7Hha7Pr4#6q;0Z+~oSmc@(a9G{JyGbTv86r=boz#Uk`SneC?d<wm=unv;(V-+f^3ALIxs;R+aq;K#^ulYDmGPmnaJQFHVoyGlz~rPp}c$fB5A#vDUwEhFPU!ud<Bmi4QVm2lK?@V20L262wBKCrY+&C5{-HIVwmp#-1dh$jX9|-mIYNE*c$b~GuIEFdI83kzOjs1oE#|lY&(xAr;mTfi`_l%0t)9D%2LGvTPQ9o-jj}()_i}0j}^+L6Xva`DeW*~%ub-lB(ZWBi+KyFdjdj1Kr?F6yguQWPcjS|DJgQo(N5}RA`Z(L$>)>Q`gW2+o|0P}ESFDMIDw!LPm8n`M?8UWPx_|XQj<#PbX0ZBY3z^9qL7eN6ojKHY75F%s*`VOoWT64SUPXhfxU4ko1R}uXEvuJ$OaHAP|yH7aCgx<K$T4kia~&+kYx}tfL$N^<C-r1$mk@SC<~bYXx!82q<uHYgTS2mz?>PtbZDG>Y1;++ZqmXe!xlk(LW^fQ)4<lb3w(#ecQWCd1Esj->YT0%B;2zi7T$#6LGE7TSYHF+H5&ai<6rUllHLxO^fsE!&<R>s`V6|7KZUL=eRy-#o>B;;WX<rZT2V$g$i&e1w0XIvHDKVVw?<Y*7k34dd~<}^aCn7$<8rP|lQO(=WVWNS_57NJx4|=^W92$VZU-xeHNBr^K2{GMGhY`)z*%Q_6O&r0@n#HJb?jaz1s-T__F7R~^P?7`LO2%9?U3ZX>zdAhxC5Q&wldr>@q$tkv$Ci;$uNECEj#mCcHV!>yuXTX6d^SwPSFn4z?z&G9Non$Iu@U!!huaA0t)f4hBr#oM0{wKcc{Fhm3OT2`gxMqvjlVvtBg)oafJsWOZmDYWqujP)|~eM!&w@JW5Njg78+Zt$m(T6&?@PqOFF!yV@+1K#${tzlUH!&;AeL&bR7Y~SrmdjghErLDOKH~T1E?Aggu|J=fOT8F;E4?Km8h4L~F^G#{%fg2Iz2r4g$nKeTM^dasawDzE!WisJ;XyZK$8Mmlmyfh9k<UpS73v%5@ZUU!M=q5K*MnpY!<&U%fdKmz4=6Z^<Gci!NHCMQg=6<Qa5I*+B$=A|-kIC~rX$?OLGtTNB1!&n1XRUZf3vHCY*`4FmH%cVukAB~q&rrX><c;d_P=Us1tGPUDPIZ_vqP5v@EP;_@3ApoQ=&K1^NGFfj9?!P&r#JkY}vHJZ#_#pDv#8z<-R7Pl1qU{Y*GR`ra~?QP5b%BpT}Yma#)wG}XPV=cFp&b`vJueAJ8d%TTvRsD?NXG@*X)VATD`sKhc<*q&sV2Ipd+g1+nti!G59f(k_YRw<F$FP)O4CSnX2@j~#LtJ~dg#w`v!x3pua7aKA<Rml)$v)BeQe6xezIq8P>+nqPKS$V9JjX#By?ev%6pNzzo0QfvYV46v_{pfduC<2C8{!O-h&ml=5UzsoHTsaG3tefY(Bs6&>}Z*IwyEd2S{@y$>Y05lQ*CfWHNad)4OSE_n{xHqF&YbW|1bd|T_*AV;l0Gdu%w$kFkOp4%v!z2H&DbjnuedR0ji9CdY{bsB;PuapO{DPqS#yWfGf>IPCgGgOYxAC$wQ9dA!h*|au(ttXBH1RGkD0E#Y0Xm4<Y6{Y9<d+u3kHXhjPkf^N=%}hnxj?$jRm*xr8jsL3!?81iN(wvX3lSAhC*Xjz_Bm^*O@8AJjFjvfxj-dNA&7f+)3aCZ28xmuZ@d7M@Be`@8^A0>;9%9P^Augz0`W@8l}-FYp5OAiaL#xz9G9RU75s?2}!@L`%PdtM>n(``ZM7k%uJQ{KJP~N+&e#ap?CF16az|hsul5zw|(Krv9+k^l=c#+<6uZ0axKsUYsDA13>EvSPAzeF2;O{&b;to=#F2bDud4l9*$vmjHv3CP2BfWHQsCfocnhP9vPz8HvgV>P=C`x`GRyy8>`3^N%deMPuU?wM*J|x{zv(m{*Y~5)D4kZjd6aB<&1S`;-}tO63X1aQwdW_nF{t3?*4yKF{G8bJ5ps#sb%nVD*==vTMX>SH1xWTx}IVT_Cr=Rl-n_=v1sY$xggF>Ywq+Jh$15-0OtYGFz)q3%;z0S3;^;Jf(|6itf)mh-y~6vROH1eyP?6xC>5&eD3~8SM|9dlM{L${hI`#~``)1e7AAAGQg_6r5Phm}TPQ}XEP7F*9Nal_EUlAS*g&R$5+17-?m7k~1tjd7o!nTJ+)!4alfnrZ?XxLIZfzCzsoGJ?+V5|YfoN57mb9p-9<5o3nHwsy;3p^LmOX<8RkLQmRLZq~gzoIE@2vAfydX|J=MhiLxsKdQ>lVOIg3g4RpM*Gh6}}MK;cIf_%Jd}jG&DIzUEnAdTTSR?3YtN1Kpun^!%NOo;3jEzL&d!7f_aH?RYNrUz6Yc<c&4KtWFiA843M_m;bJQboCykRV*+v=+48GqCEF?{D(fS|0hBDalQUJeTG`qp(;$f+L;7R&CI<Dv{j#XAqu2f}D{8;iWFcIst@S@bFg++agHh~@i=cmOtXh4c3imYBGKX8>!F3MRbOt55FdtGfP-BLaduSrbw1FV7rriTDICss)-I6ZEcM&ShF+gEA2*+NSh*?5w2Nf{Qy@yvJ0S}F05jlNyAZBkIVK_Q>R|QJQL|e$n)P`=-;o`rP?f8>4PD8!IibYz<U;#4?L#wpHl}Z+Ma!@6lG6Y-*FwWwLTuiPQ`2}vSH^R`pp=NDTFH}0~XdbgO59g-{3_A#;fNbugq*Xme23HEPVsSdO=0_Ds;3@rEk%D7t`5Rqo#1vJLWSq`6*#tda_%E^6rAAFXLu0nftYyQ!bp0XBprLnToi5>NztBC(+U&9H*~8cc;2_3y`IN{!C1X=u)u$z%mO~8(O5EJC60M;Hko(+Vm(1xE9T&a)l;idSbq)@k+(uufVSX~15CdWjKy;#oOq*(vxr|0}K=p>%Thk!CI9OT%xH#g19ETn^PUYk<+&sns{wbC07IF5#YIUqTk|ZQskwa>&666K)!m?5Kv@|GDnM|WWv79sjZ9^fR9QLzj6#CuKm0$QQm$9=397!DDR0Eco{&u06YC={sz<{f#zD;*a2_d7B^n6f7N&B5uU@j=5FH(TylWK|nWO_fQNwg&G^?I|$UX@c!W)(6F;8=Vc|IiKt%{l0~)ZZpOGjuT_%Q!-Na`YZ@_Jnuw@8L!~o}kQmujT_|lE+w#V4~yOWLQDc554h)g$6yS^H`#KPp@crU}Ub7RNH9xW^Or($`^++Ql7?<uQ^A)296ZlSN1x+#^RP9)H*z65>f2#vDYPS%PZ__66z}s^%X$X`^H}BpmmQ1*}#e<+lyB(A6n%?K~xw3BlkLb0ez$8R*GTTn3a+uH|Zke#iSL1{FRl5rVY@X7}wD@{96TJ+wgCdi5sp&=T*I*+xibac?fSYfp{NsC()B2^pZ)0xAAxT7pvU8mjX8=)<w>WP0pdK%)5?5cUO8d*;A^6J1PMVrjq!UL@K~@Gzy2O#W9h^fA~YH&Vyk<5w$gx0VUOb#qds9w@^%(SfJFosRplS_0&{u_+G)lU%R;rEM#QqkqmGtw~1t0P6Vf&nCGCNq->Zz?&s2r9<ed^6WOzNw7`s2=cHNd#VAwxb*)M1<D?v!`m63CO%r2$VcBia!_4sR(@M}52qzBE<l%QTLxE%n8FWo&5*0czJ=-z<!yev)w>EP~Ol(7=vmD2apb?~tV)0VR785rhr(=OItl+A>q+AyEI-<h=7>TkYP3y)!pU~v(tP$}vB&^+7+T9+DF9O%Bp|_w*K3@to9A!h`sT{1Y1Y2^mKvDohTc(Ezz}2fd*Cb}nO*LCIKAeE4^G503&<wxF!KG?NURSRn=U9Ij1R*jZ?&Oko@v2LDxJQ0ZtV{@Ph2OKeXV*(=h1Q)In8_0PHDitd?{L_9o9~6<B8q65=;5v(cGENzo@|J0s{42z_S~{%(o{lFtGaC$Q{{}x2$r(x$XXdwO2;euB8-ccdkIHe)Ca<GtnTs840x?zqIXl9D;Z7P2;ls4g>hq(U@ZDbHMpul3`I4ALaR0@q;M&znklT~n(mG5aJ*JUlc~avRT#RQTefcarzE$DRDpG~K+Tk8$gHqO0sKDxm{x>G@WU}Bnq*wU;Gvcw`Bn`E$JC_$sv>aWxsDSfE%y{YNCAls^w7jcHi~WO$cXMX3>SHAG17aY<YO%4=>yPes&u58SfB}QJ*XQ0O$@jO4bAGoV;mTbqU+fdE#H--<wa?l)vBCvrV!G^kjU3XQL=QT0N+8bEukW#stS^9o3F_q^bTyj!gx6Ia?|gb&k*Ym5P!^$@Ree^3p*V0AmeN7=(NF__$F@nAuqs+t2P|X#@HR+M1GX)JL&mAFSL|*bvcH%z0wQKz8I5zE5=atp6H5RRvBQ#C;I%$yj{axxwS3$tW#fd>sDL$ndiec)cj*&*91D_JlTesf2_<sa}%I5O4>kY9gCYlXOwhh!L*;<L;LOkmCJYUdzf<h*RjoUH%eawNYKu$VqJ+aZbOtob%Fm3J%lIZc&oar{3s>kUdD6I|GbSI^6!7}U~9t^`syC%Rq77YRqFoI^9<HcimB^a&o%A`q0pe4Y#=|z9t-;N@uUt0>5Kr=03=Psif4FMfVN<KhPY(iVGzy>WgHkTRj=$@45A2*LRN|WaU9<86EUrbGD;izlkgTG{f_%)b?AG?@?eklul-m%Wy^$8BPir0*rD$oJYy-dysk83H;nBY1lYONq!Shv<DR~DN@A=k{EXs2-6L<DIv6A<WzoE4Reus|+SEPef1}%u@_lZM#=S`-g90E_zNy1AD1p@)CL1SE%1?sc1}CQ}b<2%gVY1w<g!XRvtMMyVMv{e`xG0$d&z;QV#3>d{d}tV-<T;V+G#i&}a<qhLQ&DC`;*m_CeR&&{1rrZ_g<;0X`z^3AD}zmxzVBx&4P-oB(boXm-aDbYS;{zqJi3;KVQ}B`ntGsvv$V-qsTI%kN6fe&{ygPqA3b-pHk|A>l9lofEx>p_kpzW}F_NK7UBkalNn9PWZkqIVhatZjR>t$-EO&oi$Vm!`>jCCHUKj5%z;e|0Lh(FHF_Bk~5&=j~5_O%M(1cV}VrVB3ge$3{dW)~z(a1xgQFH-5FEZ0<oi|-w=MC!AdW0d0s?{x?BZ(qXH}q5|Ni}`7jGhbB&@^U|#kxiT5R>AmeT?bsz@>qP_Np8{`6ao+1M}_s_+Y#%)ZY3YI|xE^a`6B|{5q)>a_C{I7)8qv6~uUuzrVpJlM#m|A_7@?bgc%9tmV`v9ph7PXqYznbi{fnnl?$K$}S$Xk@D=syNUt8Hfz<`i<5h!muNtO@q00PS;Cijs#TnGbQ3MCNsnJ)mPCgzd<Cb<Z=UiVmeL30SLT%Hqy4(y5;ykDo0=$6pSVM0x}GJ5KjKoJKXHTXk*M{!++esE!`-k?;Y198N_@-KpJ-!#hMNet;}8A#MgtRE4*2C(qd7x3O(z&5DLV1I9$_u2?6CFwmY<L}!T0rOyYhoXppi_F-%*Ivs`>RkGhagzcaBI~v0?-CevkxP7ds@tzt_H|Iq5i7Baro3c7>bl3VlC@WePiN_UqAO-uTBKTZr?F&kP|7a=ErULTgSjSu5$jEB#5W-)oFB+(Q$FlZN5QKMTQ#gZR^6$e{=yqN2oYMYdqB7*YJ3T=<{T^p@4{VW3wGH-z><t9;8JdB>(N-IfutUV}++Hq1q8c$FTYA&4riZ*(-XZr&mGy3g_XcFUJn$;M3s1(>s2#sZ_9Fo##%0Z|v-^dh+CU4fP$E|E1CNh-t-&lB@W<Xw6gN(*0<fKUE#m3FiU>8<m|r;X$Nlh!Fa-rv3b>f~_uberwLqICPW<F4;ASfxUbu408j#D4ozmyM==9I&x>0rK(EWx<rWcoidH-Zh33_AdkW&5wR6-tL7?4E>%r`bcZo!zV7FwPy`zt#QP@*El{tJbAj!c4<jua!I7t;y|?pnpvnC@zezoYK^O1U9_6?ypIaf8f5ySaR=mNv0H+ES8h1AX(!js+rJ}9^*kO%zURfDNV+|Dn{ll1Nnm^&IrQkAQPvp8e)$t|Ifvmxen`V9z7q^xWaHa^9(keu{;^FvR6fdGKLnlBT-kZk82*~awdPHm?KLS_0<{`K?QZBH(&Vqs4P%uQ^|VVNiJmEM7pY}}bVHf?j-+k$yy1m=`wQ`S^4JC0>%U<|*^AOP8}M}`O<wF8Jv<tE{U8JwArN(P`%8R*ln9!lC%UPq+fq41Jmc4{H1a`W1akx3D7>*CAev@o&`<3@9)aYkZM-9q&fPcSootX4u?zU9fIG0;>A3#2%ZdfQ*P&)Bad6;Yd%YrETrU6--ANc+gT$n%W^f^&(<xFN1y@>FAKq{`=65USH5PikshHI|>&baMgKi(0ItHwIeL4i)&~FjkiH7^5$@DtlIt(B<^e$cOKlP;FP<^1t00njey}*}H!(b>llUD@FjixXT#CH1;%#Z=egEJ3mr)b#pFUEc!r14m2V=NwoQxNrYS{0=_Fwbyv3N+*ofFmb9OSa}S=xC}@??}35x4*;?lFaS;BkJw?{onkW_kn9?svlMA$8UZO{g~i8rQWrF;fJWy0Wz>g0QtJ^2qb0%3eOn+dLwqQcbp;|#c5)0C%9a!v5|WNWBSF^hZRhA9my6CKtUL~H?Y?58-l2%Q-k>&C^WJ6u;iZ6Gxx|UV$B4KxOnMU%vMcNKpl^|bNjP&&S#uEKqJ`}@kTxNw8r3%1O4gwmws>R4o8_1uPL99V)&vIVd3>6?&-t$6DaS93!t)QATqp}L0&;j?vzH>pk*d@@H#cE`3sGFjt>3H5Z6YvR*D6?8;n>#fOUpN?zDIN^Gn#;(G2!S6kZF3YZe>o`{i;!^hgZ8nqDB)@a{NHPI|0#;JL$iaDzbj`3dGILsAAg^!*4u*NpmhvRO}<@Vgp&;bu#a$ao=`Sx*E@f^lOT&1m!oMp*QNaZ2XJjVFAz#ix4tAOJ1r%fu4CoqSytX3lN#$*rH;^mkR6Teg{Ic@=h*ZI)P9Cr<zXS~1lPYO&-Pm#Ec()E1Zg<szhACq_Zr2FVc)-HBEVjez=<;26&>coSMFG9V_!XhRV6+x%_sHfLM9yvt3j_N{LiHyvLUc&=?k#MVtGiDL+Ps%idW7d3I8nVVK-6m+zL)+KU&J<)uKhnstna=K>OPLv`&IVsGUbX$C;@1RqR@+|c+tEjV`p;2msG{7GClN3z*rZyQY=*FPjYGna2T3ZIh%=i?G2DxDTMnKyYcfWJvW!XISTG`KZ))Fk67_c-3nT&{HXsfbP9ZGfVr~t&~AQgiyhz&rY9c?Qkm_BF7DhGUt;lqWADxK|U+4}8zcYFa|M%L}41rTG3^jj&mPV&y}Ih|xR>@2P^!7Ss7<F;w5vMD;ztW!Eo`R#oa9Rom?M?>LCN79~DFWO^Lt+p+Tm3G-5M0mSHuU~Ruu0;|+!x6CouC-?RjZFVc8zg)TvM+5vRN#eSCR#O(Loc;;EQ&#CgZbP>qy5NhcSrT@#KMwQ@QTM$fW9Xdl&o?b8TbX9?vJ-Mn~XN79<05vIQI}Ps0Qs}5KN+NWk#__hA(g1;xiqx{2UhAGB$~>6USl+eh#_^>{b#_ijSFcuw}agulpMI=b)|N{-ryG?c-S7SOnPsi$cwCj=<vRo8jyscm=cAt*x@Ivnr~HPx$Sw@~gfz(_x|;L^a(Tf>$f8;@MVBKM58YmM4Xis_XE&PO7eHsl2A3w-jonUU5>vvaX-`GMZOb_RW!x$6WQwrpPkvrWe#D^F9!Drdz9!L1D)2xmu?CF#72ieKgXR*dJpdBlo(>VRPr8dz_|aOt}#$NKCWNja7%py`tAaD4Bt%Z>s3WMI=Cb;W{c}fWjl9sl1RqIw_H2;*XPu9A!MriE8>)3f)&Z=-QPGd|&0_i)P2`>MAx$(R>j_*eokEq{@5rn8sYs(>uJHxUm5$B`S{;&|S@F;JH$cU~f3+Rm8nydt+Jr;-vY7LaRA*`Ndg;Uz{v{addt`cLPY#_yvyy+$^4Pbe_RdT0Mlc4A1Nk(N`Ab8As=t1m#yVP_`=?IKRrp`P=3jXL-IE_%VeW&@JJ}9e@H_tD9dy`r){b&nVm&QnTq@P^3p<SFyp|*<p@d$PtAcvrsNC65#CH55#fQ;0rvZ@L$4uaATz*w_^HrEtT$2`E+{yr8(NY$u%9np*V4omc0pH%f+f?Y|tzXy=piaZzLd;d-QjO0O0qVlDboob$N=&m2+*XqdM;p;;*1Hof|7nbiSiHpQJlfKAm1qUA*djf!*&=_dC@6FR=R^>V7BbescYIO!sF*hoNv;cKC~H({)*KG1U?GB5IcJGKc!bgkw>agYd<KV^K8+!F)-g_=SeV7ZM3P2%;9#m8M#yiB@TnU5TQ<b9b~Vy;n!!nE3apmOd5fX3v;0tF(LS32-$X<!pJxoOK%tOJ*&f@Go#`tkAO-fH|KP^5@OVlG)5#<CiTd%@WBsJY~if%W+T!4nhl1a-c+NoW&M^|C7vl@dY0tnipU25xPk^$xp)I)sy@H5Og?SEV{%Vz$7IFvgi_rbZ$i24UQw>lD?SGyM96w9V-+&L_*#!=bBXU8!CRoi{F^V(_QE}SRC89M}Jocz&-qH&I&B}C}E9~!6lHXWQI<h#$4j4xl>YdsHmn-NysBkoJJ;b8fpR-T}7ORm>p^2G}QDgx;JL=EaEhXIFt{6R|o(Sr(qMPF^f2j%%#n;v5DhL*c+y%*AA;{kuMSOF>Lqj=YzE7zpHsmYRTmEryeGht!NE?`1hdJE3AbEyCKDbMyJ$P`N=u#&h|ke`j|D51R?C=@CY?_KL8GVWDjdw7yymaexljuI`Oy-`1SB+K%oIU#`yN@&<~UqICeX2v=v2`o!KbR33|RqCH(6EJ)Cx@oggxba635^p&J0VU*i=369`(NJsh3F8ULnoBd?pz1)6nl|8@*el7iTo$i4JLX(+tHn(pw@4UHnfYdjP%)4OimhRrxS2?RY2B&MUQCZ0gTAVq73<DQWz9Eik$O*im++93!ppbo2$LgKvaQ=?26bOLVNDx3$M+pp2qy>{ToMxkkhkDnEey{SnWG6;|Sh(B>!Xvv>w(f^o<gDX|z!srhxHsMD}&z;$!i@g5G^FLK`*crCDE$NG?-$jbwel@<B4(SM2o~E7O{(R#15<b8HiEWCFh#kca?0FINj}@QR*g1&Brw%(RnZ+>xu`Ipojt4=^iy!gg=OvRpuG~pm#33zw^XLB#pJwwybi_D=ejtoBJYEj~#^*Km&7b|0eeRS@a%;ghY0iLDbMd%+j}DWI2W|{n<n7Pc5AlR3Vev`Zj{-bUX`Zq(w-;ht_{!t$&-5};JnbNN!UqFZm_~5`LhSyAS!w`{^R@$eNDhy~YZXU_h4iO)BSd7?!d%A;qnBz*A56m_TIDku*r_qR{ne!=AE4Y#TSf~meDl};NzoC8pm-d_q5r02mgZ4msVt{7j1rW*1V$?v=&Nh-$kqOYI0w;zAwofeqnuNLjJ!E@9334fKjw_w#A8@2SZv;Y4N^I<iqYvGl*2n+)1e!(BN$GzNKZ&WJki}_#gqNx2Kp`rzz-I%9v0o3PGC0dnK=XRnvl7U-Ag<&Ek5(E8ESc9*R_D~Ta)A(5nWJ6cLyN+fc^IlPt18pJcUDu;?O5PMfao79YO=sj!8xSP&%<!@JgI2o+}>!v_GP^MbdYC5*}v7gk&dBytwjt$;|9f1ajfa0~70UHC=%Cd4x;`|37kd8H`9J?}QU##Dv)8V>gOu_5mwR5}c@bJ3@CX>^bH^(XM~{3%ksf*CB`_S9A;(Vpe?a=|rJ|_&m9q5KOXx7a<n*thk)C@oW^88$Kt1U&QL!GfL6vGtP#8{hPo1uV~CANqVS`Wc9LrKW@Lqvo$FEi@#&v_i>lUS|A|Pf)t7mU@afH6Dt1G|H4j%Mc;r(UdV*w&(S6M_7`r%>U(;TD?h~9@y&nu8PIPya1+@(?X_b+9%AmU8(z359nwX*M1SE>2ZYr{BIc85YSFPs7o9^6Vl$f-DmoQm2ceneCLS$xbAlbX+Il$>;`Yo7qX`{Anz=f|>WWRtDAf-GygXSrz)zYjeC0ArNp0gCKMVSMt5G+kxhL1Y-~Q7#U;Wr9Ar8cl2m3A#<r-^9KP9eC6@U9vx3q1nV$@(8o$h#><Vp|AO~SIl6r`XWA7FsLU`Nx5izf#BMrPtLfY&hP3T|^9y6(F}j}*7Vlh*$E!T$N}zdzYMM8T$cQ||4z_IF#2y;EzYgsOCl1SyEV2N8J(e9T&OFvj@uVASa)7ep;((MDWV!zyj8s}9RGXEC`tg2IhgHZD>2B{g5Sy-7sGZ)whCzy0s+-~PQ_s6({w2A$C7bmKgSW&go0dqFaXH_UJ2V6m_DV&qFuP?T@bnw;(uouz}~-37tqtui7a>eqN2di!%!6Lp|8*)(@nHSdf<!%z+fJHGwZxWW~eNG}u9^2rCO>E8YdMWViNLJ>SdC3Q7+xjrGvt+7wNVI|!YIw?aoO59DP2Ja$Q=&*xJTn(heN~y3=0?*MR?q1~eKn6Fb7hVVogwczu3-UnnB3!jFxKzOQqqw3Mp|i=t?T<sxMZZfFzy>>t*NP{vFQ~C@5R-3>=<CNIa$?_NM_jF}7m*963@Pc2FMU`D)`Zg#Xh8+-3FS7Pa0-v9ru3L9o}u6g*kp|s1%KpgssvS%s#jy;p);A(z6{+63kt1E6cZ}0KBicRFE3du3#dgN=rKU*6-KMLgG~ka^ZfRg7gLvnl?kmsr47|C`U{Oo`NRlBG4=}jxWb;g9en&ah>~h!AaGkJMiBX3=%8zKjCooIlzUl3K29T~`3UW)sFshpuNmIxMmk2^<*AROhJI-y)}KZ~QrPat3YCb$l;Jew!)E)NG4vZJxx^bDdW13XN0;kZ{u}%uP$AbWH3u@9<72=_+e20I-`1*(4woGO&c^_8r5>+vFYF6JNo=H-=g#h3ySO!S(R(fAV}{<efL|vRa~RzfVHiJ3V<pB?Oo6T(Nztio(r^+14Xb%Xn=lw;7$FzS!`2Kr8Ym$g$5~7a=4r_ELAR=8Y+=O1-?WD*H(tT62%1agUSbPi#r1D~^pi~-W|9jd()nB@)YF>~_OjM)(1Q)6(!uum{3I4}g)$bfQ_#Gdgn&^MiBcc+6SfFhrG9*nDig&+qfE1Plt>tIFXQ%z+n=-!k5BC^^i{)txAsqN|NQoUN#&zo98R(G+rMZX?k3s77vzl>26DTvt4d@TV<)W0ML%f1#w^rp4?1~uX)uI)36AWiDFDKh(C&|7TUYyhn|;}L-y$4o4EVD1_BX%QU<9BJ3EPzahUD}~a2eq65T9zC2C^Rz_{gftjX-1&>M6Ssu&ZPhSn2^B%8Y1=JDxz?q!5l6-Z;lfb}muMG?EF2jBNW@6XRT=q70j^S@tom0Nu$v22%kRO(Z+B3uc?gF1;+{n3kHD#u~$6mSGG{Nb~GsGmT=JKlco?7=6vNiXq0mh0J2yIflHeGmK)`ml@WuS*9?p7p(YcX@({2Pw|tZz$j98wgK!MKg;y!)_nWd5qu<N7c_n~Apuub9(n~shc0UN;t@8VafkBa0jS+`jb6<duyey+zSZlQ=U(10vVG;+yq>`a*Xq0RVm7aw8$sFTE{yybt<wCYosqOU%r<x-{m|aE7y6*I=G(i7!f5WIg5!L17YPa&5=4j56EO3PU0F49OkF1dFI8-!eI&=ub&j8mpr)-{du86-d>a=9AuR7@0pg}Ev~O{28ePy*qB4fwi}Fledxt0N`}Bh<Wmvh+T|e@A%De>wnQh#9A}*F7#fCAgfS8_R)0%10;xG2)8?~O`M8QBvGYnc!fKSMjmBn$UEsMsCGZNOyv}W<n02Q8l9d;IUUu#wg)0m}MGiAH%8Rq4hvX1Eo!w1Uq4Ovg<YQ-6*&9Go`F$e;^j9U#fXuXU5O5Li@F<(9RHGa{pS4V-{BjXkHEZcVFg>*@jxp}6m_ztEkt_QXFHK#eID=*u0#fn1Pm|?U+3o@)T%NnfsGbOXkRh%&8J?U<6O1|6g%Ub2^F<N5E*h6-N1z?EI#6$2D`Ddn;YX4++ALh2WZ7U2^`+GC&Q+vmW$1JkLAx2>kmZ}*hD(QgxF)}jC(%v%cQ*!+}r<;V>77r&f(=z4d8>Tofo$~u0`8FwTi;|7!+oZIhN_i$J=<KTIVf?Wc;UZ;`(xwm<&M-&eC3db-D3~dG)af)%MkLQ3B?>hso~90_j8K}AjN`6HYDn9mxSp1hKbjS)IlZ{Ry(|b^OiA0I(Coyx8#$VyU}K*)LSf_s<-VS8gyK6%kiXs6u=(LG1YKjf$gn?&XPPFwQl{A{xg>|8ofXevPj|!UE->JeV{{U#&*^x0lWTF}st#YVM8Qm}Q+hQ(n-l7lxO;cX&=&iikKxI=?(x)}UU-=Xrvvz4%_&}&E>g49qZPKxO&#Rp4v=P<orW$70nt4&IiY6F739R`gw&$DZ;{(aBg}+B>3HB7R|}&++}9uDl{7RsdGn1-5kLY`AuKW|VM`QqpWm2)U!o-uwLxz&*QQjfmPh`08Y`m@Q9{g#_$pu<Wqz?c(#Q^DEgCH=&oVOLyrQvKFQY2KD1b9i0EQ&rcqHt97I|=-wiy;-!eGREN_RCWmK$nQDIBnQ922eOxt1f4e0~1{*AGnqi1{NeN2F&ln%N5(jhgTar%7Ta;(E_)YtejLQNE?<^sIGw+&IcH6+Lg9pTLTjYbZKwVHk>8h9X@tQN|wAO(bO?%B-WVu+Os$8LE(G86t}iv-Fn?yU<f_?1>A$T#^GvDju3+7ScF@=P=5VwxI9G$FjH|RrBa@Z~wgAJlo&J$Jk#`p)a8wQuX;RpT`O7c_5Ox-IhPLx6L*&C|>M=@>W}A(=iRmZ+=}^<+pe<++&Kr{Ril`ejS{vWt1-MRH}77o|<fWQ#4)6YWs6i?s)6M5ZDW>69nG45QO}#49ZBgo<x7M+jgqiZGUCA?Hb1tyk&j$kj*<8&5wfKbcojt711jjvhO?^At8W4?iCJHc*32BzV0FIPl9lSr@R=aMq(h+j;R5Wm8QK=Ow)s3TUUtG4Ma9(^ME{yg~9%N4I8BaOHTOvOni(0MG_UKA~~_<<e-v}<Ooy-a%}QobAr6sQ8>_V9;Xmfv2n9?^_np~0+)=)x@w=ksv&Vy`)JHzc(Q^HpK&<#1UB5M3J*$o^qu0M?cP%eHDqv{U3zp*WTuFc+yJ)ls!6<n6iebo$Ef6EL}+yrq$tjcb_b86*3CjJ^@w7ET6IIAw!X0xYUeKZkU8*a%{`}(GXLL?+kFc~@d}y1PZUU@n0nezLouPAqoY`xi{hV7y$)wFQ2xd)<K7tE_Ui;i3_`fe+f^i_{502@Z-rmfB!*=^sshEW>;b+uWMMQ6y5eXFHsJu3tb15Sn}~XdoFqF#G#F?(%cAwwOtc(o_p3a#RCbzN+HL%dv8+|9)y%O>B!mjsxF-A(j!^AE3pq!HY)d1$JWuu!Sw2mo>zg*75PIW?R8kG2GQK3Mh*Y14(yoBQPcuQ0f~_-t`@v^QcENV<2cNNBt+_Nlpm9$?DTwL5v10oiI&I8bT!4MY{ZQDU&u)KN?s?_?q1SiG6-7ue%-a{umJdjD@Mbf_Sl*?1MYLMNS@rqjC=53lej{YdQNuaI-jhbsieZ@{&^Gdx<&)q1qry#W_Q#r9($Z(4Zlqzt2;WlkFjGIWA1hJ|wOXgQ49v1fw&&meEz}QDW1zSP<o%Fn3_OkRQ};wuxe8nAiKJ}i-<mg$d=m2J(DaRtib{=Asbp(Uj4XLbS?~R1td(1HwJPB#O5T}b4(us}$j;B`RiIoXtS3?uB({`lId7zt8skduSc!o+Mj$<A9tLSLtSe1w9tJ3pK{@byE;^ayp)s2fgJ~y=W!DphZhfvom+&l(2l@i*8ve6sM{#P7hOgnmj{!5a?TxvJBp&mbSjaQQSvc@hoTW(O%p-~9RvjOHkg_0QBvL6}k))ZAkijdn5TeJsW@2;Yb&S|9iI{U1MrS{o&~AgK54lL|xZvSZOSUi@ndGpGPM+Fy^Ic+8S9{d-HgP(ZxSagvpBZ<(PW-J6bgUCBSmLMScsaB(_$k>lZ7wmxIHHSSdHYuhiWwW~-=D=QLFe~osUnnqw+j`a@H<?l^!9&eixeR-e~H?>(-P(6Em2Ns1}5)!fpW4Js9X#dTAnuVx;!~EmZ!NWz5m6@$y=Oqarsb7lasqN<)ZT87A9xz!n80_Gnb{UcUYF3*~=0k2>88x_<=4*Z&X-gGQpDoI*Dq=ZtShHrazhvwG{R-`()e;*3Lbc29QEQ4L-~@X}nmz8)J-%;*-<UR{N~++0kiZ4}(YOzbjbI7qJt)>liPf&&p@p>`S_3&SP>@8<io3SM#p1`#wMzx#OujJc7h2p6fn_Juljw{Wl(_8MWx%eiAs-Qy05OLC@PZF~KDH9&GnDJ~$)3pcVuTiNg^DyFH^xg(v{f(=i;Uh4~MEXq1o-LE`J4-nPo3pByn_cfw431JrtMD8rnJ6V7dR+Ii)5<BA(a{)Kw4GKs-~*Mj6(kl&?qeFwb*;ZMN|JGaf>9<YMWrBY#jwckMMhLJiB-n<#|z=pWOCSfu$#BQ?iaKU8;(Uckj)pSyE-vnvokuDJOOCCT$kPweeV}E=meSPW0;));fmy2a}QA)Z5mymgL@<hA^(f)Vyiivy}YO_Uy(faOih$h9PU29I*1pwZQm!fCr#5<>3SVV`Nl};cf*I>#4^n*@mUFEs#l0Ox1><|wC@zfJ^T4bwkyViD$a_C~$ayx3v0P+$fkNm-Y$R##EE4-Y1>U&oxddWo&iY8H7WE$4sN5}M4IK=V#%Ha(t6^Ur0(IB`w5MFL%IHy$fYU_u@?^;=MpWL0sXXs*7HPaf`K02zrQAi<9ZwQAQ-a7eUeIB4sW36(3HA%zpf9@orAdVVh{^$%ip4=A`#CRY-3XQAg3{W;cKxB_2E!B@GurN{?L1>UW)98l#9vR8#Z!wBA8FfYpia&ThPMRF9Q~BR(w)gfA8lN0tsq@BhQ!pWh5#6TO)K_J+EPVd`X)P<!F%s!c^|{Ag_>=TO5M`tefv;3dMGPpML_*>H)q|e!hjO*pB`;n|iGe3hv>YZ}A9`AnI=WVY9pkVFdj&H{BS-+i1mCE_7$FsJ`~r%+L^{Ez8Ih6JG7$B!8-U`4slSb}v7s1-!``MJ0-90Jjoo2@58fP|?lzA0n=fe5qQ&7Q7jnr{A40}Y!XOUNx4ANKqth!8dH76Od{gPda25r`RTHIBNk*6v`7ey@mv?PMbSVLkhcL*1MVa$ZzW9Tu3ZS@fM=~Z^@Bb(7?V8(2l0~t1{fZX$+#R$CKmhn5iX3W!BK37vLorCsXtZ2jP6KEFEdkxw?gj~HRu20(!jJZY9X<}njj$v9;HMKlw&VIZ?6=+b^CQkL@K11N)^~Mv1C&O4j>8)}BDy;(t12riD=RB2lcI_Ru@}tqae}Tprx)IAoKiM`UWOr?V8b~jZyp{4hLEAN*1i`|Y*pZ|0r2gc6BhlMYe&HZHf5QY2Oq)=1s(=h$2i59ZD2AVpfY!Q(b8k@D9W>?cSh@Ooko6^%aIoy^Y+}GrC>RDXqbmnl4h?Fij)@Qa#?6_!N03Gc9It*Vx~apESbRsqs(3BIl5>Q1hkisqndyk0+rI)Y!LPHUy;WUU4yqo4L!cSWG^*-vZ#Q0rBwAQOjv<f3TR(C!a4}Y+Y5t}QM3Hkkd`$W`@H@^3w{3Z55HUn&5u|3PrLc}`s%?SK0R#VRXYH~5a=yfW3-}59%un7L0apf2elwqK@K%z!XYTw%78KR`op@TO8=o%(JTt}95jM<5C6TR@ZazTvohE@Y7q;o#$N7={?_WPjqiL6?ylz>XWs}Ew!SlT=c_-wY(3cc?%)5-FQ4lEpDzD!^@l%PJ%ssP`@<jp=C?IH<Fns-55l%y(_f0<Rns8v!$vI*Z($2OdbXI=YyTbvpCAlK!oR8c4c6d2_NU<qM@-@$oMoT(o!J2>{-BV{dAdYD+#*ldAsDGmG+<PyMbE8p5%%kxf%O=e_c?em9w*Ic<|!&ru}1;G-m$TOralY$V>Q6|8bl9{mPEpSa6Ul*PFmiC%V?u>MNBDb;AGaTHPTzN{zw@lr3s2$+<#0!PT{s!kZA4sUMe?m0dUHG-sVclI?GKF>K9v%-e;pw?4Ig3!Gzo+!ZZU7Ky*XLZtc>jfUks+RnjYNEQ?|XIqetL&htD;0j!1EF$k=B4Fk_KQORviIEq?B7jH0nxZw83Uj5n^8x~O4!Wb7IQSDjy$2ofS9(V!^OTGPSfHS6vGpN3?F)^Xf@lR~CFS=h|Brid=s{g`oOU)zP0q`*W8MKdWXH_d3vfAsE;l9SpH10-zg5fT0KCVGJUk0!^FE4O2dl(PoDEfLxIdXcIi$69Bwx>V5!hA|lMdk%*2wXIRK|{yheUFaLL1^ICeZplidb;9HhhgN7ilpCQ9B)9toQtEFE{vdia0)nY(+H#z%ns&BENH+p>9h<hLew|n)D_li(ZcfrY~5VFfi*$3$)r)j^J>Sio5$4dw7sWO{Si8^(ep$4NEC#Dt0{l&6X<wtkG~;jU?hdy%HzRBh=x%{j8>~vQ<r=hq*puar4gco4$|#(b_<)u+Ca|-7-o^dWtdC`n$xacv<%d%ZEgSgA3cm5b<VQ;AS8Ro0^(D`6ovC&{=?s)i(?*ozeh-X{Jqzoqrp-8_D+0zC%&~Y`wxa|^YIfsnf|!7|L1@BFaH;Q-&c#(wA0@G{qMc{U;evpx7Gd2-#@~unR^_VeG|9fcu^BnMMpGNCRF%gUDDMOzIA|!!$<#8S1GTo&4sSE-3F5nA*Nj&Bz;Q9)xtzsd3XVYdrRNy@(bRkY<MRyE!e)kb^h|r+v|&GKVA4LL~;zD+0*S99ii&=m`q^2rdAA!BciDLzP*lO(14gGIec%ir)QH8>oz11hlAyT{c80mNrw7LE$gSzEN^7_auPOZ9yd@?1*o9G{P-J}sN*-I&Tf3w_zkyPG)HMPX#9r!lbgLDj)A-UvUu5Pa4VXKxR00+039QZcnV&CXyH@cZzx?_3=9XO)s6qwJI6<rR+UVwioTg^hiRco<-EH>jZ41o5Ia2WQA~DB{8yCN<9{0<*rE|0Sni3|V{DIb7%ldw-{kOLr!?uettcLZi#NkMhxCyi^PvUn0^Hy~xPi<!wKU0)uqdR<a~jtqJ%moyF6k26RpXLW&M^rJc!Eh5!1~z>Cs#GUs5*rc#fsWQ1C=txnRZzttSAXIwD_p-)~<?bydV{7bCVV*REK~t>do`8j;MVzrt5tH?mNN{TN^XMOri*JlXx)E{u^Sb5Voe+@jd#tinYYAPj--YhXN;d<RM!be|RO=LzgyRY@#iN<bMCa`*O_{^>u3xz~ge$o?2D*ovx;8rO@i@)@>P><gvXH1cvg)z7X??%>>G^OlM66)6jSM9?NQ~mC~f2+^;ZEfMK?=e;a}VH0jk8HU|(U#?$3#kdNz0?|p+#;!KSOq&!99pHYlq+RM~hHEqr5&v6BV(&fn<2nQD@RvdjK3}Il}rQB;^E~sG?EBVZ-fqyRv+hufh<=7&@_ac*K#XdH?n_%*FJL)yPj=Qs}2hy;E>k;rc%n|cDrRh#+Ce(cE+krIftfY?mV7HL)+%UN%En5TF1)ayiEE^}f+OIa8pbp1)EcpT!{&^bK^&RJZy|i!R8ie8OXp+PspIFQ??b;e9(`l5iSqU3`wGTvVVT)}sqT#Y`0wYZ=0HZCwkqIwsNmDbErv@^8e%sJ8p7(a!FQ6ia__{35K1&O>OpoZvfc*0r=uRQh<LNxlY3E@q%kCjFX^QPf3<9v;!@RltFu~kz+ntufW)#u3-k;z5Redk%xz)8Wg?3F5%48IGyG)j`TVQqB<PN<EKUX;@9LyAmn9S;CQFT0GY^+O%Ia|hk6!>W}$)2all)MA#(hftnO3(WtG?&g%M5+Eb#H(9qF*t;kYWXp&pdLCIxTt53jf;Av4D;F4)5hc9B=x?6PsmP7ze@Wy?BStm*L!t(<UNI5(g=2RKi^Wavlg1Be)b-E;<-PDZiVPxbOUAR%M6<ReVApzDE!&~3Ju1kqDRf5`|{^Z7a;=f^UndJ8eaNO<w)tAhe{pvg!RtgJ-!~Y?lIj<Dg`yEC&=1ZA&oec3`NI5Z(ABs7*f#`g%gi-3n&?V5vh~l#oEm8cdOU#oUPADBj7ApPLg2oMRX$rsJ4!M84cAwtfYi&bK!hJ^<SlV`74b;q1EMO@6vv09S+mf-0CEgumvxZv|dC0S96_BC{J%J!R?{9TAKO}rMHYtT+&Np6n$>`ELk!BPUgA!iPdP$WYDPvu*yQLX-=A*S|tEw25XK<Pvp$q8%h=p`?RRxb#~j1Rg7h>#Y$hr@5vHOmeuv8il&AOGlvW0KIakGJK>=>?Ar$CX!MekOD#zH+>#corz3T|TY^g2{lpJ$i}Mjw?16toyF$IzY|=SJZv>1C&8yXXZUHk4cT};XiA+%Am^M2NZ^Zxh=&z1|%EP<}(!(56uM=T@Q!83t#^Hk5;Q*XjnL2iZcxI_^q2~eLG!IBq+KZ)G_$tm3^s;>gds_AbIAF)fAvLmrI|8^<1n$|uT>;#+fj_a0x7FGw2i{I~W0ffm({`?CEC=p3ye)raV>$3v1Daqr_MXvbdt9b+ROke<{xBW&g75xN|3mhm{)fSa4}Tl3-wz{e+@=+MpE82C%R4+}RBo5|a(cOGLws^93n^tcL$N=Szk2f5{U|#LPU@+zJ&g2+o?m3$$$Uy_(7K&2CP2lwIqlY?&Ne1W9nnMkQ5PS21>uiHpLm_kZHF&s$)cc+46RA|$x@Nx0h8il1%gpL4)Q>>pOPbHBR0JFVc!;a{5_kqY}>0%TwO?c920GjX+&ggvKM;$Ei%}-uhh9aU{%r;pLElP`Kg6J*>~AifnH*iaMUMsguA9iqh^|05R8m>IPm6auwQkuEXrAy!$@CP$edBK<mi&qEJO{##^aOb1FhxFq-Jp^VYABpdj+{9aTyN9Kv3%gabkHj656GK;YZ<_tJEz0?SWyavMZ5LmLIe6wV@;QUCl6^V-ecr@9TIk_pNrrOs`^22CMLTEiqhlixp{3zPuK_Kq<}H4%s3(-!@lMylii+Fce5!ah%U)IEInsop=Fis%E~b+Fr{I_S10iB24f$#<K9OxcR08>PG>no54lGK3kqL`+9=CqD-(HBTTta;^V;C$KfzR^2l9Er#|el4`UBh=}8o#7Xm}eeH^3Aqn*kWLp{YwPF}2D1S~<WO}W<}C$PA;3~cCbRYVnf3H+04__BF=6WxS>Gmj=-GEcqaHuesWe%G=Vxd@L@&O#V#rG}PunyZr-az4-AM)|nzc44uP)3iE(q=n>#W^Fg*42*Nv$OBrxKfuvT!-1kVBIKg2fB=?XX8}i5z8jLw%>BwWt%`kgMp(m%MkbVWwgu?6W_O_DjKU>^_4%6aM5mfkMiRZjIt|ty)so@*mb~LtZK8ll_4RA=o%p!4Er9Qrd5Eph1MciDW+@#dE@PG_oT#?pnIds5!ABeHEXpwU?0f>s03U*s45s$+hG9xoVCK1l7TOihc<<C4w%S}XL<8BHnQ`ji6%Qv02SlH@x>XvC*Il|?%TuX!SlnH?K$n(!p4Mx2*gkZU{fvR-+JZsKwKb8u=phwL{dycoI~T!!x>+b^w_CV*{^>khT2vLtY-U}PT~{!ytzb>rj>@P;j+_S2U^;v9p@7MxNAVOhjzK~D5)(J~=VErEU@&-wX}n&eJ7NqHzs4H~f=1cl!W&cB32%^7!kgBBc8$dirTDaePdBvvindp~-K7TD^@^|V_Gfk6_DJX6BI)uev<i<l9F|V3#ySLXEn%yT>PfuXI9)t#(QVG28(+Q9ZB1L#4Yk5Rn<D;NgWsrS(~hpvY92vq|M^$7&aWcC=XOW;_T=MT*Ji=}!U$^;P1wPCxrVo^ELX12o9(u5$&0UWl=!HHNdYK;JS8LuQ_R0jS2r6JQMBP{={_1f2LwKA*Wp=Q_uobN*El{@LXw<b@m3)D63WSC<xB?-QJ4KZFHWcWBZVthkI`VEKeAK^>iLG^5bUW`>mXr%+|wrbqTwwY-p7U)!><^A#_${JI1Wcevtfk70k?N8hIeB_aU{Klrn6&lj@GxnLtof;Rhtb0bu$p&h=Kt!lCDypv`$^5k>0JK;q@9`U+)582XZm&0>FjqEfG<pQ3rYh|9yo27G3xa|9$Kha3k$`@7)C)v(Q{cL9=1O&_(>c`WWam209I*^e6iF9Xtn<Aq9qoftu%Gis>ijnd#((cIIxY?LF`S1^kQU(e}S&zuy_R>iPgoP~(Mwfq$Ahc6g;dnOE{MEdM=vlTCv~og!8A&~ywKwx|hx&AF@xo5KsTJ#S;<nmwqI%4UB|^Ex8aoo!@SVG~7Ar?1eND{OAr4wV#=mu@s@<Y~&^@{XJIX8XXr***Z~F8tBm*W?k_LUgR3WOY`<<%cWZ_LxnV0xpZ<3b+AXm!hF~fQ6bg6!?2#Zj=dE(92-Q3?ldmc6ir3i{LBvS%6j7(<RYzyzl{Mx?m4@SN0*+xnC%k@p8N=1gu&^h#X}}lf#nKplw{~2+<QfLE|sz`?qYAeL2|pw(N|<I2e#zL?s(|G1_td8O+e=a2Uh(W}Y1dvwA<7G`#dxe41xJi61ag(l_%QCf<+11a~1A|NV!VIZbfa%*zS4P5tXfa`RvXz3(twsz-r0+d5PfzZ%dM4Ho}balYAQJCxX%Vla6sp<GUuvE@}M86Ai2;_aJjm<$i_F5W{=sbJWc%Lttvfhed?{#fT7gtwA5^qUc;P5(!!4>MP?ENicg2<Qnl>NCP;R2FYJ|NB+QKi#pz@3FfPh>4Ex{X5T4Htj)Wg{ZZ#9@GUf8mc?;=X-N{mX~>d)!<asia1Ult1-w1tg2O1<!b1slFb*J4;YDe5}xPb>@8hwr#V658b+hd7Naa2WrX=QNDXHiDRDk_KoERv`!F0#%<3vW7kBL<A0uLe;nU6<K-mZ<Aa9Oig1MLkk+>&Daas_p0n|4nI$jkqM7P@gw{6}R%V1wn6@GKdVmIgm`;jreSGYRs;_9rxrSH~0f=D`mA|Q=F8uDm3iDm{>5pvJF4}U&`s^;v|2}%<X>MEIhM8O6U5}6rjP&VTPU`GH(>&-K(TzicQqC!imr_?FAi=qkYZP?@Mja+Qx`tmfve=m|5sAkC|B+Z!p#F%Z?f<t-NbbV>F!G8n)b#^rr-k)IHjp;It24_ljf+k>&Uuc6l@hBPDOHh0?P!!QkY_y3lSR9R$bijcLy(Y+o!u621+J}$r)}yYDVw{?~->%jhR=J=<LvLAA#!ZwBFuRJS&VkubjWxI%H9Dpvi;A@t@?&$Cj>iE^MUPXAJjs>l_~2^@4dIbwXS)1=f+#_v_)Hffspc-vmGLB}cx!mwwt-Ji$;yHcc{0;J!ISu8UF4a^PpOpzHIFeZ9D}me+KhEMgDwji!jnt84PG0)&al_Ah^@Jrn(%Ar_P|tnUu$!Zu2!&)6n8YpWuy)OiUp!+Xk*$C{H&i0QVb!?R)pACDy9f;PkMb?@sO=i7|k$t4sPb77zLlzgWjuHZizUf4;FSe`vk;4(;u2NsG+}#3p9bf3c>dX0{@j89vzxaz8LHiQiEKIJRy>MB0^>EieT#c1!bI2;xbLD_bWVVLc05c`nlc?6*_}|mD6_2{C_Y85f#_S&)tO<F9lsTaLPZRp_?r6Eqh$<7m7SpMW{ki2;Ykrg<`i<6V~^DO}8dh^MGbq!@FIo&ou8g_-BMI;(AKJPjy^RHC*bm#Pw9-Ql>aId)dxjuHn#7YL1ZqOw&b=!nQt8Y_b>1KBekcl;yIaykc5%SYb!m%6c6|?eH)-<(u`vLQ!w9<fJO>Y~!T@=CmYWEU34N#MlZ-3e!;A?h=W;71VGS{`3W6k`$m!C_pX&DHRRQDVLd)@}!#ZpIM1|VwIxb?{y6BVw^ju7#nT<=N(GDSIba&F&a2liiSb|xqhMd>?gimLkFV+NwnZ@9;0~|ee>!t#2CS?f%pFVW8BtfR$M7)0P5Pdsa4k@a05-{nE{@H`+=T}h+C9VY>)kB0RZ)q7@Xi}SW<o_3eQ|6(ebloWNb2aLIGyY%brhy_yZXoG7Q4G4aj!+%;ac-EIeY->2T!{6zU%Hmjwdpi1l4KCl;n3DOm5M1~+S!B}qY4%t6#IB2*1z_-Wbe$^eviZZ%=?Wq?YJ1_o`&pDs#Lx>ZCsTxmeA)p0FGfvm}PbXCYpPH#zuPM1@G5@pxXoY`q@`gl=V!gPx;-B#C^qLgpbUWYfZhtYI8{+{<h|3cShHHs-=#IZ2pr`u^H8ZH+#^7{por`qowSj4ineo`$#w@gqAEno}kqa5fB4=q7;wEQwni;bKrVDv*b{agLehPZGLZQ$tLffCkc@^i>y)Lk!<#-|za8QuDH&$c^?svKrX92N~#i{e=udq7Zwf8zERZfE@H+W_y10Ogjsk51!&)=t=4n_HGyhUF<);>B%*o+G14coq!mAL-;}1Tr%3kFS~igCq*c++LUmm{|`YSf)ih)oti=*)QzMPW9ahRLpi|r}_p3-<svJ6pcZ0gbE!X>pv3c`6LOH!Pef~k@3F@Ow#i`qvw01XAXZ&)=C$!CgO#owBK5w*^jADr!bfB)snx$erZQy%VHtw`G!#l@f7?ykVlwdN*zBCU+|Yp!}kUDVJzP}9Rsn%n=FqkW>ICkvT%VJr+L;-@3$UbF1Yg&>QD*KuWZH!nw&wk$~<my>>c<qa+=uf5sTW!iq`;)O|N4EbtDjQ56s9WD$2|dW<m}=>gezwq@gB7=L*fK;;DUQm9;0(-B^YzsAvkPzlWB^IdufB<hd=R-^T)~1b_mf3#PbyA7jJS<E#)QGGB7|cP9M168O1>zjK9rDe<@Qu>h~(*Wuquc-=<uhFd!st3k<&YYKU_fFJXjVVR(fO-=`)A5EJD+r{Jy*C#yBz;gI;jz@QdVO}sH#IM6x@WXgHOLFa~`$r7L@uxp|(!Nc{`wQ>k0TtWF2B_auqj<b$w1ypxlf|HI8X7(_)nOA20t~~qbU3$VS{)<;X7`uYJ~Be03fN?=#r5p$@VI;Y?1jsa5YhRBVcM1)gQix=4p)|o0UZum2mAu9CJ>k;f?5nw<Q52yFeKV>g^9Gmjwg(lI5V#HKWhS3O)cFDE$q}WH$%te2J80{q|9P1r1Ckb%5<$YRx!gV6n#ed!*N?YjbI7I@Pe?Z%+ar&BsULpo$1mT5J>&`QtSnWlLYoqKw~rjZ)4z7BKMUgpl|uE`WCm<3X=?obDI@MhqMF*dwH8(m5azM`dTA|E+3qEGlP3G#lG6-*!+%<A4^B*ESj1I%P6K~=a>+dpa1Bp*?BMwv53B?V0IK;qiv-_VIgF@w#N<19gElZP>aI+#pb>&m~nIZ&ep!-og8&AzN8yG;RQhXgEsNZ$AcbYugQ|zRxuSi_GLZ+Eg*%q{w!Mkv%aS#?7YPn2|J%OybDth2<eheQ)0Xq<vyxcYVmQDR-eePJZ>-O0`V%iJ24tNoM%Ec58`f}6to6Y?zG7+&vp&jxnQuYh<ShxJ=c#EJ$X)S9rPoY6;J4m_ho1FRu!Lq<%w2yUhg;ufA2gyH^t?OVzD|(H;NSw6xYDx@)#&7CaWxI^(U7frgNTfVbqp_hJNu`#?McT5H1x+xU?3S)T2b#Ymk4buS5f-WfQ`H3#<&livkM-5CWf>W~3d39&5AgPMBg&*srj#vIKDpTSKC42-#J%UZn`|X3j2LB1&o6k;;tL25OUXFaq#adXf+=QEu{z3(5F=j9P4bRQ4p6lMQWu0>H}B=IyZ)A3R>!RTeB#+XSVLu_9<IksH(gVqzP1R_c9Ba22PkaOn~2tk--ZDJ#9|(D=<J`GL5yO|PFOxp*yAMT&wzZ;#k06o{pfNs+jLnY%3G);P#8SK0w^OM(l8q!VUm3*(?S2?umBN{z!4ebhDxr+K`a@dRT<q&&OXXW>m*J9&dOOP@xG4V^`7-r2PI#7c!nwn2r=s9W|(_3qbbK`{Ycp%ID`o`(SjmtzOVI*afR?0DH^68?$#$eB2qb0+VN66bmm_HEw^V!vRC;|y7`MaoOpu$>8y$(hcecF*}NYe>At?HUW3L>Nt5P>Jc{cqssA$>W-D6Ae$m!r59iFg5#5l|1EP180V@lG7QO)=gyiAPt~aYc~v5l_{%qPa<7xXvG<bE<ChGD#67*k|@vT@O$FDIrFk)5)C|-y&R9oKipHqN<&+v>#<&2+7}o2wigBK*a}$J=8(gb7`e$?id>w8lFW@LqL>X&1_b33RRTu#6k25#u)B;GXupt;CFT_RzBIv?Zt#g|WXM62&X+~&f>_DPNQb9SnNs2D4-4(O=hd4zDB}6TCkh@Ny%meU^H>;K`w-gDU?vmjDn4na-gv@i`n<`m)5#|9*HuGtnRRxnA;XiyHIWH^E<yI`vzg@msv%d$xvcLE(Qf{u?2yz1r*mKD@u*kg^~^~j>Clkk!5|0M?mion8YNxnw6tly)nxNj4i?*AXl>El4lGMPlLmH4Rk!XaVOinV5)M*r%)f>paX6qB7$q$-vlQnKOwUyNJ#$c9MM;mk_oY=-ll-qSjr!!yk%~E#R?VS4`HiG(-ZTUOO6@T}hG|YG6qrwyNyb3ac3`bS9TED*bv1Tnec=7x;VrGLxgf9kT@B6HTH%^4Cl_qKG(6gVN5}p|>PDZ+n}LkoWIGPKA+!*X?JwoM3Mre8Jd%NtdE5s5V}z&~3}zUKxykSj{h__7)+DV*hVan#nu8^!9-)xS`E3}+YB<mWCG_Au?;O>O21XI&qk{q6Ju9)TzB|okL43wGQwREvRNyy^WYn!wx-qU9sZ`iW0l3KYGryfJQ-U<SW##v;D`6JgY7Wgdr@I1K7C}t!ck|A-_X{B1^KfZc!e8hdH(Y$uHUmP})Y2NOthAU5nz0mJ<=4jKiMOeHL~;QQ!%Gg4k_l-4yk7vq?XWSb1t_TbWx<lF_7lPpS+w3xTJ78Cbx^6;DQyc^2du*Zr*;jzlsv@Y+=iV)DJ{58is=;#H5H_ln*E}snn<P_ay}P>VOd%|>v<{OVRorf%yvghR^ed&kk|wpi%C1dAsX@M)vAsY5bHVnDZ0*F`9&|*q2X#&)R{Yx(riVqL~^c;#X(K0If|TYE}8UHcMGbh08o+)_?zh9FfD!=o`S_w+aXs9A1l$iQv~f4L=dhcMH#fSUxac9Aq(u+o$0J)Uo_PPit@Scy!oQ*UMi@qz-GQc9+Yp)G~C+H;<(`uU6Vu8YB0_6#bFDKtp-RVK7YB2avY2iPdt1UbFYD^ioFeHbzOe`bs6lgy{p7g?AJXbk4ZAo<IF#g^5zAG5Bpt|V_1h%jA8|Pl#1-|x6#OZidl6xysmc|#ZcLH^MZ~p*%cCavDKtIHDvgB5zI%SUvMjiil7Qs0-cL34^-2o`1AdRKVF0(SvyCq9Df;SAlSzP-PzXg4sLk6)^P^_ok2&B<vkWzRI9y(r^*GdI&7u&#muV<l;ro2q^h)KxB~Cu6F*`W4Uwk-<axrn`YmiD3Mtnp*0qroWhR-5y)gTZdJ|B`vj4s5y)SXRW+;UBHG9$r!=u9b>5W$-uiaYlyCzhy#hfrjIEo{VH<}or=7~cv+6joBD?olX4>Oz~h1JZfk#)6Z<xzF|$rBMQuWD^F8~&zixXkCXi8!x2kI<8orrc>V2~v@<w&29QQ#`SYe;1k-ee{(h#xcM?oMRkDG&Jh&Csg*KXCCZ)ct&@bc!>>O1Ns8#9VBx!ijBj#WHO7Zg!<te-*lz@({WUA;D*;{+DqfkA!`j?JUpNlI`17OLv+12+qPlfLuAycaz=omY0buw^s=!I=2`Q3NR=V^XtM&QIR(4JfbcU&iBg{<aj1okQ}S#P#ez9kG%#^QtB$->VG!eZ{v#QJYG)Tjfj11mt=6{b)B>G&9;Fm)lJ)YkePw-r9q6AqEwrpq>NMjB(>n_HR$#apC30goO>aX?Rj}c~q^2`;y^dtE#KHTiz#!twJLi{InOGVM9Hf~8j0Rgq0a-H-XafU?+j@P^&w3qQsco!ml(P_70o;XndpV2ff<(WZ(*J<F5xTXzyKjF1Ee0Jk8GARqx)`3O97x;aSKZP&P{^%&TDs$nz_@`owjQb?<d)Byu<s_H#;BJ6Od0KpC4^^9IpG|NkZ>DK$XuXWRT7TGeWwL)vw-O8Y}ro!S*csKf_c00s=(V{>8=3XnBdOT<Xc)?<twiZ0Q9eVb71DUH!!QdHE`>`6@bHMLoQcCI-RQ!q9Dd87_VX{l+K11(=ER~AQ^~z{^MFG8JAxWnCX5@w@YV1pu>h;us^GGq;fT(s-}0w_fL-d32*rYg<Io-!drer;dZ%(Tkx0gqWe0*XAWS&S)XRS@YkmzE1c<EFw$%Pt>w1=cBS9`Tg!3(ZJFo(x@XO9Z}7K<JNR4OA6%XyH~9&2$#Ja^WCeHdJ9&fOd8k&9U%6|m=E;7_=h%2bPUaPk-=&yjLC4GTlP;z?!A^+oEekJ=4fF|r$UVXP!7Q`lZa9xeb+%Wa&QsSSC{#ixie<134#6xn>!71E&`NXwQHk!}U3fw&8BZ<uUdGaGjlq9nPu5}pMK7F1xih9-UcIuNl_{WsrW2c*%2Vigv~+`T)#Pab<3$z53&MC&h4I2Rxdq&gp!PBEDV~ZxeZ*a1Bd7?L!v%P3#1)~pq8#T=TgvEd!;Po$A{%ofR1-fn=}{LloQ>~{lPMzwq@stM<1MriMqr3A0s}S4>CYf$f?Jlh4Oz;cs*ur4DKz7P23GXK<&hy~kh>WLwlz7q1nsBKm~>TQSQDL!H5%HGYQJNBHdPmk`2&4$m(#|#p$}PXKCW99A7UF*Nm((V4P%Uqr@NJn<s)mxN<*#7l=`>P=rA6TwH1v}VJ6H$rYRLqut{5IW{>Lu4+~_4L-@+3&byj9$sEx&0$-&Jjk0`vk!d$Q4UC99gnh%?MjOcE*0$+852`bsX>XcgD1jz0g1_fi!(XENC$<7zp|_Qlqto)bO+<c%=Ff28o##lUsVD5}8pik0=xDWNFg~Pv)Lmoi34=QLiHEDg-|wpJ90!D@BHU$@(ODSjHar=eOa#Eh@+twq;3p9(0gD9~C+*bohtT)w)I`3kKee196x^rJZvJPszWEiJ&j;-sFO5@8MLR>!eI@D~7U#U|lcAn51(LCk?#bs|qztFQVi{s)$5O(J^>A4(X>30){a9tbICozymtMj^JF#m!Zxp<Nq4>SR28}2!yn6Y=?5e@`Vl;aC$9KBJ?_IWFJ-J8H>B#F7Gm(C^S8u-ZwUO~5T7{5})!OZIsx$feD9RY;(_KgYeaZN$29O`GxLMp2cfssSV<qsp0UwpYGapAzLt4NEIm-$#UqV4K`Sbl%!T;`XFz~wGjc|*El_W!t$a*t)*hRvT4_<vkJW;HNc57#f_lRdA%7eKS9ntbmmxzTF6W3P)(-tnGJnmYn!;A-Sobd?VGsg+a3@4YW?Q-_Pj^W`5RV$qIToG#Jw{F=tYYP+1jx1iBEr{dza$M!@9L&zvt0g@`5;F;@U7Nx45nRg2<D_Vj(n6fgs=`28@uVpZr1M5YKeNK2<8CdsLZ9o7$nDGQsz4oD%pwYMn>EDGES3`%-{PZn3n1;>37OD___aTYlx|V!XuD--CCxc*?OCe;Q9j}z>=&!%ky#Cn^%qxEWTa1@Ip$_eJ8Q5_F+zh_8phWRD<k=46|fxxwp)pp!*&I11zwzy4MA`IqryVgZ5iGoN5LfOr2%bjFk|41`HwJ>_ha)U!Rzwh2kD2<h?+1$pfz;m9*Z5Pxk2!)jF$4C=eTDY18mLr>`$f>gR;sU>vE!N>~A`>!Ra|Kx|(OJc*cS%JVUtQ?cg@TjKlj@ZqGRMhP^34sAH)B3shSssuAvHw#|ZraFPdN`Dkwo69@m<X<t=@`rUG#w)aU-`#_hGw|&`WQ_?OlCN4lWd5dMgpdgM!+xrfq4Q%s!y;k8fR(PYN@FoQ;aF<2WoF<fp&~+)AZbX|z?4aNBCalPeRC>M%j`D<$9^w@-!U}PTi!0Fh#Am@Lou4edG?|rQ!03|eV3@~G%P`F2ixLb~;XF_767Trr%Of4<PZKQjDjs6e#-$bbcfnltc6<S+JRRV<;nf!yS+&2Qd>aeDP@0ABsVM%sqWE$}<!pLF$z`#mtXMzd<H}+-@8uvee{9Ai5T_&%>p)Quo5M80I8^UE@|nO9qO*r69)t^+2^$?>!-w=+KBp1~EL+QQF<VJ*altZ*(%h<Zcxts3#aZKsDdUJKdEmfblOwd9aKhyrLq3&L|AS9KA9wd1h0tnsBF*`|tj?R*<mh~}5RU*2MZQIK1f&n|!v-)UzM$MI@SR0if2^1Or2TdeqD~L}IMrh8@j`S`%7jHmYvg#T3yLMav}Z+67N$0^P|iKN`^le|M$F@vOxY3ZB2#xnE~Apo9SfH1D%hjSDhi?)s;Y7HvgEED3aP3Z%L{_oTG7WQ(x^EoUT8(RwyL#-!d9>|x_G_t=r%dtV9UJQahQe_A$^RAmNU{`!Uc;?X$>c7?OIUdf)os1$EL81%cNy&ip!YfrMW419XllENrlLa4Y74%v;2uIHDkYs!H}D76tAmLELS%|Nl#a4r~Fj%?qsFFJFz6*39pJ~U;J-I=$+hE>YaR!*mKd}B#SFPogn9lF1=0|0daz#Z~;cImW2raQTA++<JB7PKx>Y=cG<%?fHa0a^|4JUu(Z!7_II?{>8N_N&N4<qwec|`z;fnWyO>Z$joMIaUA%U;WN~7AbmQA};5)0rCqG*3FX`q=br7<^2!sK}Y{()X5UqO4eFwZ{`wVkds_1|sJ+InTOGrqD%8)FTA(<+}f~``+)p6iDA?EoUY~2cMDEIG(ZnJXbS{Ip)0r$|i0C5Wo-fed^7;HdpH=Pl#K1WA?U%D>Ym2)M7?NnsEeA6;eRpzBC^S-JKS1lSsRp3AFP)5YpUr~lB6b+#r@E><5BZBLfnmgoe-uKaHkDE;z4C$W4-JqkUJ^Hu7v<S@3^LCHz__bHZdwd1_wEq>;yY9B|viFPEUAzwTV-(&}M(k(t2m@x-&!SN@Xwv=hS1~(D9(WgN5NE)4Q)DD4^*l-YuvuZZgT6+BSLE)|M9a5M2MZZ*w|2FI*61)BpQg#k0>^lrj@P|#@N_;LlKZ^%9>W;0L{T`e_<LBzUIV5=8E$Er%};}r?zjKKE^iA{^fXNIXr9f-WpKNPN3M^$><%6oGSF(Vy~AFJQ~N!yv%M|u_T@o33iCbhQkZHQ-cGB1bx+(AmtF(YAm4g52;&@7zq;ujFm<`ic7$<zdf7&;xdWQb<+l9QQ7=3Et<LV#qT2#C;QRR`k7ko4C4w~@kw~{OcQd3!WA|o2rr{5=JHd~l<*A3uQSTCg9(Y?QbvpVB^5TP+UF&5RUv642H?On|jS?ljIPe0b&jYM)1AcGO?+*Rm1&{|=1wM4T^kvh5iP}P#IvS>J4bx)-(`FT>F2mH-FzslVI;^oA(^eIxO@?Vx!}LhU)X_0*>zIt}qJY%R3?wn|4%1nJS+jr7&sX6;4EvhoXDS4QBaI*juyP6VxBC`%o6K+Ub$=g!ZsE^nM(j)!%ohTRh9)DZZB?K{)DgR=DUlMMKdv(iPQx^tfnbbo!ul||S)QTL59n0`W<Wskep0jVcxegau0CXa1wp{wEI0zwJ48X(5g#adh;aW7(+ydH=ra^mqFGxsQd2(>kmxd0&rCSfp-w!x53w%~pivqC5miNyrFTTZIx}r!(FcX1t2pX)l6*MKfB(a*9xlTMzvLz8h_Yk2kaxeZcTErAD8}b-sXlbX2NV#)kLp8LeCS@8sUJ;MdALA)SkzROhZJ*sIN8VA#IKM1mkJs<pZ&ycHa6hrJN5JTY)toyfoQNI3_$+)G3G1gr4W>t!n<`s9U+|%sW7BS>U3B){766FsUU<Il7qkg2_Y5?Sc9M}z3lZngkb1?GW?M&!el_03<#51gvp378IU7e%3mM(Fa5p_MYGSarXjjLX4t^tQm>NY*R%JylgbtZYd~Pb*?ZhbGHeT@8a6jvGDFUaY_ZRth-tGWe?p0m_47w2N}6@5j<Fi%h*<Kc4n2M3Pu(l65}F@#Q3=hjxv1nZRWg^AY_dw`MkRBjlDV@I);j1sJ?*fk<-RtBn?O5#at@6;hDII3LLF7pwVzC9(S($*G?>;$lOvS=H`#gGhna(aO!;?%VxFK{?6B{A91Oyg6>R<Z?Cj#%PuJ%!509UT)MxBVMqua39JJB;O~$J*KzLI)!kbJx7QD|OK*M5RL62i6cZ7<4JbLr}>8sbzuFo$HFMc@pMebgy1WGYc*@Ne2hcCW=c5<<@55r8*r@Rlt_4+Wpb020*SJrzWM$l+Zkmo^v%v*znknXD>h9(5)<{t!d1aNkV1E@YRRP6ifS0}%#=n{W{C5rrsCQ{l;h~1B+Gxvk|hK@=HNq;^CDS@qdHVN_P)8(r{y*8RO8Bk4cIWGs|kN?DSc;Xl?a+UU(lL40=8>o(Poko*xtpTDw0O=G=q9EI&Yv!OuOlIR?kL`W%kaCuf*(dLl){2p4Bhq$E2<HqjSlN=#ZHVXGtm#c0O^B$AJd86KlX~sVv-9ha(fFE<wyx(<oYx8=+U{d%gO);wpqKP!8@C2O|K<kNFdS-p=F!Vw*Oi9-h+dDQ(Rc<+GiXOD&%1XM_BXxYdX{9xmvK7PUQ$VTo7~8Y<nuVf9WpH~-u(JzR`LM@4@@+roK<k6*Q&kMs>Qdg-W$E%n<N?lZqSc);|~<y@@~<+iPs478{gHbdkrmoI6>n}y#F_AEtVhk_fS7uE;s8O5$bFPIXu=L+)wE3Le9EAO|pol+yRjUir&slOUlp2AP#?}LA-Gd;*E0<Z(M^&@bha}@k+h~lU_JT?2ioN{5nnMqj9XoYPJDDo&}Rh)Gzx!2I)HuW@Vq>gH)Vrlgj?ypG33oVX&&c{}|X@xP?ECl1Y-v!!hbDZw!5@GZcexWO3Uj#j-zyal;49s7EoVAMKL!|CY{d0{E!{?hx4S4hvgt1K$Q9$^|fRE*V31C_zWN0NhWb+*6nz6Xq@z>Fn62O5q3(cDA-LVxHL7MT<IhrNJ5rTa8IDoe}Iq0_CO{oI-AV+crMzK!aM=U_eb?=R>d4HfEx@8<MJ<v(oPCp6OVx8gbey(9weS?ptz_fp;`5TA0yD@_<iSmxFY$Uyjizjpr+_(&i}OIS|Vn6@3KV3}>EkES*d!e8BUdk6u?G)3531={cpdFq<Oad_vkhv8(#gsEQ^n(3cu(^9Gx>B#byyb9#MeGC9cvjQnm-bU_?30a<RSj(I90Yr&ys4-FSPcDsH<o6K}%XE6UKCmpQ8r4FpyfDYr{M_sCa%O@A8ZMTyHo9UBa3F_%M4B6eB$Gf|9fY$DGSz^4p;Hd}RW~a5)*?z2tKw%AeaG;^FhwpXAWEE^?69@r>f<HUd(w(kv4<%_9RxtqFp;BEcwY6I;wdpF=X3~cQ*5;0pxtWW*4lRO<`T%yiCk<$`-|)<d%K^I<V7Cl#(*oR-fM$zdn&f$n_PHMm=&~{Bv@uJGfP?;+d=!~$qP83r%gw?*#SgfxYmIp+y4O&MeY(DdPSRaQt!<KkFw;!@Rt4j58gXw$;ly{+`e;wfX)g-N>W(#tC4u=RK9Vzqzu%<yn_^vQP!)xarIhXo`^6fm_3lU6ISQ2efL}zj)+Zp$MP#<ALxseAQj2(D1tKH1;C-(yy0<~=As&o(==Ua0p+T2^Q|8~nrf;10)BiS9TOQC)7YL`#_O@c=-CgV((80)&MDmTTj$3sk4_n+Q?3`THl(gFPeN$I-DQ!0y9+3RXnzyYrD}CBn1`A5&l(fu(s#~IMep$mcoe<mDXR1@FPUUL8HY5T;35`)P?y#n=(>B<Hr%`X7hYs2nzG-@~`u1z>ac+WiiMPgzin;YgYlZmo|BwC79ftK+Cg!iS-}&oqSJvE=lqvY;qTep;Ps$W|bN8`Z*nODjOZFX~{y(A1-$9k<CK+9QSBm-<=;>cWNoQ!eQv7);`Dd!EoIxXsPgt!;GOcedrO&OrN%dx{EA*SqT|-JePlJ)62q0k|pa<b5(?%Zcpf&=n^@VPMb*-%m{7TEzUrz<NLxZc<{6e#ILYFM>n)6EG*rcJXsNZS!%{`?J7!X4ZLM|+PxHM;&Rn-WcXitr%RgHp><m1)o&NZV6KSf|~#36$1PvZdN7JPPXCmg&86Hv8Nc~IAj;(@T-Kf3|VI;%7LwO=&#hjBJfLv+!3ar#63L%0;;mdP#dy>kg4u23xM#&h%IfhMMbr}m2NR?)RVLRNkUxmEc+8Z0WmV{+d;I_%KOpvjz^m-f82_4;Bt3yrskK){OG?C|a|C{U#Bd<GL^ATQ=!BnXT&Zr~QkB(!F;*G`;RNZR5U8E3j#FbdhF{yc0&*(*G*51<90(R_zgI(~O@`2DM+>*KS-w;s_AkA?UPW3t1z9j2+vH3DP0sC9@tTBOqoXtfIRbLE?H1vIWy^5mz549rIro(|8>4&Plr{o(oZXJ-wfiPjW^CP<1wT!f|`H5ie!BC9G;tzS_ABf{M)U>#ng0!BAgfxCuhub<HYs-vbzUeaQY(p*mc=}(+EA~x+qZxa-Oo$c*SEjvn~aqfz6On-=CV@R=HlP(@_keG5zxczW){_4fav*YVmCl@6LaCd4$XXgvraQ^bm*@ZsS6|``C<alKi6G>V&0aZS95SIvxFF3I6riY&@CIx;r(o5c_*3fHD{w!Zf*5gE@mKDs%8|);hl$kucy2)CF3<FwMw1I~GWGK5)Y@Xg}b(ZaDKwFKWDU(yEAjn(`o*{Azl3mJaI=x0HQ(%*aCRdrFa5BJ9&X+ZqVYP-=10jKbU@GGuU>^K~&8=Pek{Fj%?#g$PL44#Y0)1Y!{J0bZbIqZ?NR`C30`(U9#ctdTp3J8`ym?8?K1(B9ZCZfidO?0o-L92(dAT-%r4s>NBIH?U7yRZRe>9w*FqTMGh<i=>)(*UG+w!AbSdrexcvS&`aX)~6_W=YpxZ?%4=Hv6m0SEa-ZnU9J76l3K&f!fuygR<r@c6wtdU8jBS=udF7Fw{R7A$28mX$4N;$=S70{zKofmVbgp_0^k+_AHw>QMwOEW)@z6hzYn(saNSs%qkCC%lE-?`CUTz&c*u;|W;w5cy7NN_|!;xbDXuIK<Qnv8iUvS}S;f0@KvG9Ev#0bh3F24Nh)x1AxKQp&;J3O@Khj#|B-2#S5AP_|4k<{ZyaQ;vL<Q+I7w6f#sE`Fq&S8n#<t;r^Wy_LF8UISc)ffB^-RDC%sIFWfGh=<dY|w)bK(qo-BoXp7sGTB_D;Sp7_9!;_$FU0va7cypFZRl6v}h6n0*In|QM@MOsGv`6NhTEn-GLyoy27ub)QQ3~y-!Na}GI45VWxMfYjW0rhN2K8Wz+qn>I*x}GxfVdS0JlHEz`;2|T!K<=lrrSLwLD2#w;GixXqF09ZTiWxbG&L)IW{QAg$Y54xQAU{cr0)hUaL`%f?N9qYZp;su4$_$A3$B)!Qg2MMy()0yI+Pn^9{UYR6i&=wqw2?C9HIzA{(1JXsAxBbJRYKVs4#BT?hq5*5JvKFzy)rOL2I0a(@kRsd*}z^u5UrvrHn79`D`dUdN9~mxRkMhySwz)b2h|3Smffm97F+elbz1euVypgGY?Y2m$xTxR4btHDco_%NsLv$O%?t(}cdJP{z(7GD$0$cr;8G-{35ERosEE{ii;^fP(|fU;60Gw~8e#-~?IW`_K^xO(u{FG@GpD&9*z4CxpTg?Mf}nJf@vG)Hgl`^ouz+xDxDF;VS0OHqEP4+oNuTNFfas9ScrH9-fvc^zb2LmtcUydPBY-N&aslCT7%o^7*(gBM70`|L`7|MY4FMY7CSiX5`pw~mB&c@N6ZKeND8iUw%U-`ad3H`9=Av7|iKyF(D|Uht>1qQi#J|HSK<7{NUK~2pNjrSNljnvf%+%E?K1Zjk`2>PHWNY^a`dGW*sH*d*uvXrgM@2#6tTkBlPWXsU8cIR80@ls-@WCh`Hu&?o7}$8#q`N=?PiMFe8tGU;(-0p%6OnLLKs@yOGx6{P7(~N1IO2rnJ8}lm<1pP7wP0q%Eg9Qbu3?AuQW^qh=oOw>NzOLZR!jwQRlq#Rv7SimyHbd8h{?hbt7bYifGI9=1v2^FK*bg(%F<*gqtNJg`d*Tu(t|VS(M*rctN~C>#%HXcvn}&((cMaM2&n0M;{A`5%=t0=PuB!l4gEC9vZHx^+RyPMP4g}<fE+HOjKx>`STnAotE!Fg0;*~n+Xo)^)^XH~o|4<T$7La1idIRtw32tK5_TD_q^h=2mA1XSD_e_JAzO>zpE*N#M+BxHX%?Fc@@bNlt;rfHV@;N2PssIQby>9b*k#|4Kg8;?Xd?P-LwLn%eyYQjEa<0r5?HaOt8FHu#ghZivJ|gxRbSQK6BDwe#Q?QZ3;Cos8;9ZU%~rPhRn2~5LY6cepeVXib+f;~(9bn5ej|r;uZy!+hbJ#yqyA+nH4V!mZVk4>s%=?YpRlknML9tcV{Dr@9zGwK_u;v2XK5uX)c;>;0{~ABgm>HksPF^)pUrJ6<{*sv>$`3SKF@q#!JV(y;LX=7Csd_kZ?cA8ZiNSKOX(!)IdWA!PHw-?T$@UH{9o8%s^#6ay_8qf@N9&B8)mRssv9+Kfyl{iYY^T<{qQtegp)HI8ZyH)tn8n+x(?FeaZZ^Dm!Gn?VDW)z_ZF2dM6t6)UM5hd8SiwwE~b~H9wDmD9UB$WiUX6D=iP@%cZ;z6Ez_;&wSNAj7l8u%=6hZUirCWVM%)NwG3ss`-q>D%kRy(tonE}WzIb+ip^2m@6Q7TMc>VhN`Qg#CqNK^kAhfhJ>NPqLq13m`tx5Us;=hkKb*CHBcx>?YW9BK{p?^2G^#THx8ujM&n=?MSuAjcT@c!h<o~XB`O3_cUQ#~*P3v0sC1sa2m&RhrHr6e<fvG^tIJ~4kK;+$Y;X2kuVfO{F-N>>LHPiHkAypXUGPuGpdM!-5r7_Lk=f;4&0WxO8kVRM%h%HwA*x@U*Sz&jY<ui=p=es`yBC+?*z+y~Ck26}7FGKIAT+tMIhzLApT7zCJi%1)oS>G%}Gad<D%XrLk^>t_W|EWP2YuT3|0e#c=%M_hcRCE0KmQgov495317TF{FoQNC<p*=y*Jx2Iio<+2vP`Cqd9aTmcI_3y573RFquD<=5o*1WmJ{8Q<o4*R`r*8HWb`XlbHNVT=?++$y5VYd&M{tYbb`b=<TlO0LE#1+|aVzNvU`*v=o6^WVBfa2jfH~A(UMY?nB^^L6J<1i<Lk{RLgEEp7E7&25pu4m&Q3$I6A#0dLhjsmvEs!^0!`Jt?xrx(Ac2X_41U^=C=>rayemYld=cg$m@N9z+A=4b0Y6{n*i1~CDdioRv!i3tk?{2GL2C>-ggd!Xw74&7L{_-!MZBM2j@NcqmRF|3KZ$F|##eBU<`m4g&LhVhC(q4SOokG+t>qlK85&7&EV?Rlp}9Pb5^`%T&pyo)fHc=g}3+r4414KoZg$a^o4(x=j;^c;vc@t#iRAwX^oANPlkeKT=9;k#sq!Z1B)((h~;$NmV_Wl)>6?C;ROk9TY+%t6J#*nO!@k|XT`G78C0fV<mD9CUWB3i`{<>_=L-P`)AegaggegGs-M*+Ef`FrMx_9w5aqu&zjM=22>UGt7HOC8VlTZYE&QCe92y9z1q>K_RN7oPs*fS@7&>*dGTmC0uzwAAkam5qx8hahCU6tavF>jY}3{fS8X)aFFEDESjFOB0giQc4u4H6N-GaV{wt(6n6N!T?mV{=;%8uKJ_+uv#j1vyQNsV1uRHFiG`zaoI3C$hZ>vcHP|qA8jJ~Pt=nb0J;Nfq5*Nw{#MEV&_{zerb{B2CG=f%4L65uyGOzv|_RY^z_%HA=e-88vW*r7d$1oKE%uQMW?iUP_**Li+gqd696ys!mpyYE7;RGK-AbQj<WN)FfaN<TOC~uP#;78Y1KJ7xurEY}P-hY(dKURXfLYU|%Js-uCy&TvS)|ND6TThyp{o5K#tAHl?j>e99#=CQvD50@OYa59zHn(`@KD?S(Pl+#KV*0*sH)fc#Q*?>70Fdg(>>@=VEA~JIJ#$chk_0UZH}V$ap!tQ401iCK)f}Vf(7fnu!U16mFZ~esbYZ0A57Z{DgN`HPh9_}}>=}=l4kfl;$kESGhX-l*Jik{Y#+pq|9Zl|-wiu%9%JvFG#`W(`S8MKz1lyY4Gqa<sJnxLJFbO=2Z;f2#WqNqJU(<C(CLRX1dqvkd@EljlhS<h}N#_N#t2FeiMJcJ+^7yIgj9v`Qa8TS$^Pr4PG+seZ1J<Sn>!Q(U_Yee<W!Pq7lg40sR~v)xgAp)(;2ka^Si&yG=^WbrJh*RXh%XtM6qS=6=CxTpJm^mpOjvN&WCprBuF^j?b5>`-q;DU;Pw-2C`9lXySU}^DQoZ*ccJDjJX)<IX>9%&NB$$NntvxIpR16E9p22LJ70&;*%<0kWD3L~DXS>0hiR<;FZIj*BuefQ|bEj&Y3?eHMSJ56b;mfQ*+l)ixn2k~l$RJ0K4VWWhw8b?=6%JJI>km<G>TvRk#ZBmKHD^%>3-j|RZ&F4MOo2MZZ4$Ch>~))%4E;UmnHwzO6VoLlp0?z^p}{0sUk~UhcN+YnTD{ZiZtEc_VXJNKL403j{oJ=vzbN0+V8v@}XbjCT8d0c4ZJE|mQ@x`Qm%G~1TA>gDs%u;uQ7Lk%Z^S}apJFM$!PR%R<tMh-Hm?d+RG5(#b*+>-SFI|GAgg+l7Birf|HT?0uU{yF?moLKf6?_<sf{bEr#xIVOqCR818LKo_*aFPV4+0hv6Xq~40EMM+nKaRHn=?x70=8I7pR+(eX5y;!C>iSAzBA;&cKcWV*^05`eU5CKZgs{bgr4X?`JcW6TPE_&w#QS5^WH>icfK>i=sHm86R9H@nmTn%dfQ`aFS1Ej&bu!+dieYTSSZ3UD{L0N_J~3)>+va6oNU(HcJwI*_>{8#5%H7#kp*$ZC^B((JI;Obk`e{FP*!t%1UYer85;5+byFi#{^wD!t=@GI-5s%SSxP*@+7Ccdl)W-b~!kqHu!Vb-plC53Mz@aqD}#-D|d1P)O4X*zM=czDo1$$Lxx){cJCaGSRKQa<+CR&ni;URUx7cW7z6DPg=#*JGgi&7CN{iD6l{8(tzToNt!Bo}ow7RDVai|hj8kYJyOyiMzdlEP5o@*o3VgM$h%Y&k2N{1v=V}+pc|VLp^R8I+VSB1s)Jq-minjVn2R-|kKm)EmFX&aeKpL0BW<mUu;Zw+LtK5*&VBt-83H{8G+n>2+)Z^0V%7Byyr~37`ZNq@{c$>=eW?&Yq9TaIj`YFR>q~Rauu=bvj%S7GbD_wrwUkm;Yj5Qju-1J(wS-SHQ#M~>;`Y;KyoT9Ne=;u3jt@57cCJ+n;RN-srE3iyjuk~4U+-VrkfmdY{>*#{*;dQ?d;g7>%FrVagj5#6cTY_=Mj<5#FZCt>pG+og*{b*BltRA*{^E~I)zYbcYjW=EPCL2dX^aPi4MNmN4+<wwOywg6sv-~HrFy}{aN5KqcOZZ(2+Q7T=N*vOx+xKa56PERzW~U&4IX8{`qOuDh*Qi?-%u??Shk5robkN$x2cW1>zz1PmExH-taZ_i@md>fVv1$7-c<IvNf`Om(Y}l5=MUyVJJwUt<WP8fsI~x3Q4R~~*psR94(4tqaY_6;WDX_a;Ku$JuU7R#KWd2Z@mg&)e-e9euBfM?D5M{|BTQs(0jw|ut7}yKN!-~0Qgt6v4Ev{RyF&WmI3-cMw1m31Krw=pJ8O5s0-Ht<ocXrqz#7rj|m*C$t1%Id8CdpsoV*^`RAP^;4ekUeGM>|$<j~YfIp9NVK-Gn^!IE`d=R|mZb%-sG5?5(8$=&o64Moos^S(rs1!#BMwOmD)Je9CHbXv8pzjblzeWfOkE%Pdw`WYr~uvr|GP>K?yN=CiOq3sZF5Kw`Dx<hHJHw4zSZN?28T)EiCZ`3fn+9=E*nW!xX9Nen$5crT;TxOsf~%Ih9`7fF(jn;31#qfU7BpMNvKA3Q?-&tD@ym~oLxP_N)*$sGysBYF}9vkW~9Dx4`x<NfO$T07*w<;JN!_E{G47ahmDuCs-d;?WVMzdJCSlP{dX@o!b>qW7llv{~Yu+1c6sm3&P56;7tNE?3fig)ixN4TsTwiN|Qa+-0<1>NDCO|7!k0X*hEpI^Wrc=+^Kdsyu}jB{XlMb>MqO4Y)He1Jn@PVE?L)N+5$?<B0|{&VuAZoVc_z*7f?r*~t5?M^3Y}X7$Hm|HD0X_seigB5r{1h_`!;GEjapFQCZ@-*CQ`p&?k8j3@am5I=w#*RguwUAG3W7(2q@qE+Q-g)^p(4Eo#OBA@C`TDB9`(_ldELo385KsI{_s*5a9+?R-8CcrX}Yj`V9Mx#ksuiZe?dK26vh)&3rA5-WAuoj9o;WH|vb&v@S5)A4Cjp|w0x4gRz8olPTyu_JPAsa@M$$7q<Fz+)~>^raao8i{*(XdzZ_TYDCtMjNcunLtl0DY(Ma(EP@n{F;LZu0zOFdlT&jYn?i1;eK-_l6<;(?d_~dU{KF)$i-lb8+5JSpfH2wwK>BgzHj%9@FRTuI;D%mS)KJQ`3b5O-YOwy+<sWfwtiOKC#5$;xtSNLw(E*3RptNZpw$`{3k;xzg^%STjWO&UE078Xv@0o_!QuQYT1|Sw!rny#I@9MiT*de+ogr$p6OwxdjXEpXn@C@)2SDv=;+3hdU~Xl>nj7mo#)|<`cCA+D_VH@@H_f<Pm4-|%$ujlhtR=T>8KafcYtXy$WW)ltTT^&Vl?{J#pvJaA4=n=u^xKszU7Nsr(h;xBZDsMy!*@sy|Zlv78=QbN&F@UE<H_w14mT#7g4CEeJuO!0j*UVq5!>wy`)~q)Uqj`9Wq0Gv`||S=ua<%u{ed6pqT|<pc&yJp+t0T{tEldUyb=IM&G(SXwgVTE$WBSq;Bv&TCKLKJ4g|YiiPM)buX8!m+$JM<yyT&yV}z1<*oM0?&UqhI};0dZ(!V>cyGGpVziPIi3>3@Xs65V>{YDT+0t1t3(0}%ILOBJ%dLjDb){9S_gKDEy%w|8H#wX2-|^9;1indO8<wPDT@$=?TY|iGJ6;{Vczq8&jOb0*t1F*fUuh3fe3MKta4lcNGhH_Zd`IlHA$R&L-VsY=id)jjgc3xvMjj;-n=ksAJ1uHlnisW%h#HeeEW>W(ee3lB?L5xm!Ie7vR)#w2w-(uDgjryrK}~pE^2aQ;4OzF8Y*WH#F%@6R;x@dR-?tdcP)&r}r4?m55*IG5$)4$eWPP%xz6S6~qfvj7V4ysmM)tbS2gv?x7BJ_D97-L;kiD%(#nN?UCAue!0-S+XD3a|~+pRom9`V|w+~NOGsB4_Cb$eptl-|aFHg_~I_3bg}7afiQX0`9C?>EEYc6YmL<Nr;&{pj%y*NvE$e9ae%>U#YyYQv_I?Cv%CQt>9Y-M!v?1W=DbUa|Bdon5Whj~*jQfEwMc$ATnf-QEee+J$a+23z4^mvx)D{9D~d5fq>=z4zA8>yDxnbk>Y(b+BjiVQ+Gr<mgB86!t<IKo0?WUEh{M1aO%44LL+Y2qn+}YHhF!4Vvh&76TWX8*#6TEZ#9nYT_O%TqUXSb&&S!Boz{r3M3Hl=npr3QbQvZ`r_@I>(f_$`IIUMea#wcP>4AN5v4D;8<bYuH8+q`I^9j?@N3SEZWlR)UB}#pZ@#ORfCjR>4vQ0wI!Nv7U`{o@u9nuq`hrYx33Y9j^aXvcnD6pd#Wdfn>PoL$UIm`d?rdR;w+nUHlZsa&ro%-vK_)+ial_!y9x@Qd96e+l{9Cq_|310F$zogv$nML%rM7#WB!RuQ!Ykla{?R%viqiAwF7Ea6SpPVUs7Vvv-hhY7j-#9h>GS5OX^R>tht?sgE=hKH>wCCJH~Fh3d#By4L0iKfyVdfdgK7kb#>_i<>j_uNL5P8J(I*rp4cS6)q4b*X(1lmqpWx-BjyIpp!qgj1g7|}nG3EdlK;o6A?w+dkgz^x0!6boxy?%4(jf2d~gBYEaJw+Mnmf3RBIiPi@ONmb#`lq9}rhn*sq3boK@4q=hELfu?qEwOWGO8PtY834nX*h)aG}?A%g1d0E4D@Kd)%LoGHG3AL(TRSZ=Rum2)1ue{v+dI3?fpB*P<y&`G1*n81JhxLXCkvS>JHupf5b0p*2+Ze<tENXzg#$X*O0$lzakOLws=UA2QWfH95?xkrC+E@FSt=C=q|THXsdBNWPZtF&Yy=Pv@>~^Vo-3LuC!BHId)I9u|v<Qu(?&#d9y`Z=%cLlS{dGnY}pn%s`+v07nR$N0~<C*;_4W<_@||D(WQ!UelvLd=uvxz=@!FbztetH+c%2pW8ZCUn;#vc@0t2FZ8Y0{5hs1^P#3JPYAAJwr)P1VE<tcVTYxB>L{s=TkNO`nqiC5?&Ftl1duv!L?}$_&MC)m$8rp(Gm9NCZ`ndv+-dor51d3bcWs``mL^5$o7urhJxF{BW#Ax=uZ~GWLMG1vW1Ha6T5`KC@{Ee&MeQ7eaZ-6`_?8ZKpsuQ_Xl*C72o#Q#5_hHY(@dj6-246#>j9=1Yml!`hsCOUCqKCil_}<3DrZ>x?r=6B0N199~o;({KrpeU1z}bLD4G-w+VLY0Ig=-@jYQAS7dQLWRRy|m?VrUnEu$iYwPHpvgB6DD{|9vM{(+%su1Fv*k2iPdOs$`S`mA|=Ov0}3_(InP&t(6<Hw;FrND~sPpv1N_Z1X7cuMVlOOgpV$Z`wkp|Tyx3frLT1sf(;XaG$?!k1lX2+`1S1pp@g5NMM3K<i^Z0S4t_v|UT0x>dW(Qh4m_hzcrBW)bmGTv50pUNVClH5DwPTRG&dzNAs{Kd?=G<vCEnEq?6L@3CPU4g3|8MDl%VrdgyF)*rA!LqMmgMhv{Nesbk}OG_&Y8Tb4@|HivO#XgW5HHy65_BT|SZ;y?#=0gi*A{ct!lwI3hUL#>mI}R_9^}wCE|7%VDR}+3h|O3x(F9B2hNivpHg`n%*|G#x%I%mks&FQI7Qh3Kz<;FB{&r(^4r(HlNV-t~1bD)tTe(6IdqD1A|VaGMp>i1OejsCQK*645ZKKzLpckUH~|~@jlHN(Bcv3v3PZE?QjWNVqK0(3*2HJCypcLDkx$l-&10?68xSLte2PUP^;Cxx~j5f&SWJe2F<awH3H~mbamOj@_EVyVlw`=bLFq8CE?r_5&s!A-BY_Tsg+K@$^XMpFMh39r2aW=*=+5s*$|i{okv?+l@;4F`3(84c^(Zyrsh1;PQ}i`V1U<~j)D|V$1()!9y8A%dtZKw(w#znnS9wx7U=!nd9=H4zkf-Gl(3TRSf3VjxY=Z7o1R?~hj_Ql%3Iin*{2t~x-}48`|-$wUEtl_u{L6sWLj+#?e_-TVTVbq&F<#z)=sT_@3zLyjm{$Rj2W;S&vnc%(gW^58qvQmVW)`!E7)Gk3E{6}`>q$F2KCTvZi(idtw&qC-1xiOd%P3u*34152^^)`z@OcKl?uaQclgLEMOT$o=rPZ`#E4MwXdX=JHS$5iY&2)#B>2n!{FncUVlvk{h>rBM6aiX!@;q9EgL)U0oSIj!={g*<qrm$;_F8$C;7h-D)o@n*24=zeEDQ%&{dw@0e;5Sbi!KFn4rf|aiB>wBUXQx64IS2ov(xX(Fbf6xpa0|aKmYHDonGV#f5B_u>OA1hgUL02x_0;Xpa0`O|F1+4qaeB<U{d7JS*o<-N5XdooAx}Ji~{fbzx+eo!iLrL8G$QFo2u1Izj^)o)%mM8C)BYw@cS?S`I{PYscX5IMlpuz`F<)Jx5>IRoz{F|1-P=f6FBCa<;{@>9-P#=9!;VK#0+^gAcu)a|K@y1D8))`2fEQ|&lYHmNJ8(2SFl?I+BGwfiAtf8OIFI3tQ3|k4K=)Qty$#!P5Bc#J2*hJHKO*HOLaE=ir+8LWe}^pOmXewsTy|C!@OdRsHbH0+(ePBR0&I>2^e<D)8F0R#Mf*_+qgN^9ud`A+dwy9;4GO083sv>lWZ0M^VqhOoO~EjzX}7~E*qVJC7XHft>|<|begXdIj$K_0^Dh6jTN$R-0-!$a)Ef>VH`~<8XGLJ$;_+ow7uu2=ic{GKTTkXp3W!i>xOq6V$cBZyr0f{J-kfu6&gj{9SmO$<XsvqS>ynwFYV~Lj*z{HCn{wZUE&GRjj~?1TmpgR&km2f$Io8)-oHbIfz(y{D_<ywGKzQsthoIc!zOT?Z8O$-6wj*M)!=h8i>6K5vs<yQdy`5>x89^!l63HxR32H7MOWZu$rlwMeEg>clV(o#iEyMX3JMj};bS{m=mAWQz{IL1I10f(|6{Fqn+o%5Nv1JfrnQl?F2><K7z$*Iz=c<os~GSY-og2K*w_7oS;B28aOr%C?<|_0qZSInu0>(5sMYfK*28xFQgW<gT%fzd2@j7oF%3rnFed9_y?_i>bl_R8d_zxmv=|aLZy$ICcHhtrHuS0<FsdTYGu-=yxK|3vx42s?U_P))md;AUai}Dmu{shoJ@EfE0|UC)0E-s)!0uZnj!@19n0C8>O&7q;Z;x<DIk|{bjGgpLB)W6Im~qacbz`c2-Ib)%^5{|w?B6IzU&A{FZOkKoTv(OSL><Bw|F_<86pUbnM#Yt`gnZ4r9WW!4>1>{dzmv-HVLTvCGnNkRiUrGV4Mos(>okZ`nHo}`q=rZ_*ie=~qPK@}Fj;0%W|Y=5Z;0PK&m%|7X4NsM2shz?(XeiQQdIomRejxyusq=<yS_XGNvOr?u~Gn4+&RF4+GMox?5|JKnMp@^r{#bJdPMl{vGC@ZnPgL!$~#7Y70cUaJzV_ixD(SlqdTh}QaR)G?BMR?*Q#5x*_(7PfU;MW(f|iRZ7oVr^Iooln1c$mg=NAO0gC+ni=Rb!8xYWSD+-MxcnT$zazbeVIDCDVQ_@*G>IwDwd6fSy!X*$sVc*LLs)yUE#;?<KC3XTXMn8N%5?snK{B1M>F+~9(5KU<D*Xp)up)cN#TJW^Gh!MI13enH<_!E}}`dS3h+n^)Af{ju7Ea;ExW};!Yt?<{CgZ%giSNrrV9HIjF%O`V_!Q>-Byp5o`Jd=xr%V2!|`qlBXv+MKIXGiC5%dzl~Cq+*Ozl^R-op79xSd|Js^dViIhisVY-&{g>gC=YILG2szfDij1p2>>zP3`I%GZQwV^XW)7it)<7smF%o7fcu^1Ms)x?T;4<a4)XE?_g*|j7e)5>|xw<b`S?tdb%VtqP570_E{wdpcuT&rxVcteExo_nf1T<7M=S&y2W!)!_UpBxcK7{8R#9oaFOB(+J(I7^xKDs=gBwPNkFY8DS-rHH-%0}%>tc0PbW>-=*wL>fkbf}rY|qPf9)MeMBjWnh;Bp!saT%OYEPgk+KHCg4T72ky>P<&fNf?koPGGluximq%=F2i=q&Xc(LbwJyJ@f;Y~H3pp?#hj3G?+g-@-0(o*PKw`LsrQ>On20{M0oMHf37N;fWfKIkNQE!GgU;cGBJxchLvht+FpX^EGEJU+zYcU3~`qu+RwynbBE}QIP5)-??&nJp_UoFP*Opk|b$g%tb+!6#d!022sRB6WzCMky!6DoJ_>6meinDU+OK?<OD+i!?{**KJ10^#KL75YL^zTU)3DaU`1&)+plU$8BuclQcj&K6zN3EJ^HsH$g?MYG+2N4*q?@I{hs*I;0@a2e;Xt#_n5@|WYIpD%_boEK-@hWM7iN04SU)jF~cUFMBIcFRY6-mNs*HCT}H-Ta3_yJI3j(CA))ZA+iHWWB?r{Pw`Q|>S~I;D%D`0^-u-*U<M(WpIB)QFX-b6-NoEyv_>4Y=M4QaDbyB5p+@*RQgO+EjM~LmmJFPQ}z>Kl0ZDs`Hvp>>q#>EiTYY8E<1~K=l>)=qn_#x{#&+){Q*JFBrJ;yy(8jYesvzH8(T-#xeyBPJ*v#)a}!yybDhOh-Sg{JK_%pjOf*YVWDsP>>b-LK-mQiP<ETfkNY7T>MhcJJE(iOtg5CRLk0MPB`6Y)mAXwU8N{;OhrXGCM*Cq(8)i<OQgc^VITRVO$txa`RgVu%t)bsA>(7v!WfQoT+pEG}sA!W1(i>UA4%L6Gz$j42v1E%B)PY+8TYcV<(l9z=(6hs-I4yyp)iZSwfG|N|p4-;b1-qUnUvbaep+*f7)MvyeT-2MuxRUhs~anf}eC2<kCb@lgX7TlqG|}y$-@521G{Fd^kIrBym_KO3Qde6Ko=Fl2OVj_*M(rQmN?CH2@sx^EjAg<0P-MPTXlkSH|MYmT{l$(#$g;5j`s(<1+N7_a5|!)`xHjOOVtS{Qc7H92KnE$ED;ns%ain0=9D2Uhbx1xe`T;?b;2=RcYnbH*T7Q3x_SWn5YMPLAmkmQk*g6PkY2~)PN$4HmF6~JNM*k8xPGeClpj=g>jIlE;*sQG}8q6Muh_5xysPg%)$uqXfv!`Uj66i0bQB-%inu{Lf4`RYzu$Jt;7X7HLx-sFY_}x$ke+J#@E3EymR^hoz<q-@z3{6ZS{A+Pv|dFgLxgsgZcEjpM=998aiau5A`aADz5Pu85UFd5(7Dc444jK#bqzA%DGb1S;d&>K`Y=2mW2Y>ez>w2gk5qPwwTUa^dT5BDoTEt0gA%%l7_gCC;3m%K)e%8zDo4gu_J@Fd_!Qo>dc)4aoX-C)2Ux`rB;@)PlE}KEQ?9N(lpOn=5PU`S<4zPUu!cr%B+k`Li>^?)!8Hu_vTnXwjJ}>B<!!%^%`;<c2jS1v9mQZuEp$W9%rSNqQl8V?3-9~W_0u-_gyXyV<;>6E5dvk91s{xC3AzRTdx(Wvv+wEtXwmo)EPq3C9{M!JJN5oFj7rCKyCZXNY%xIJQp5NEP5*uQ7(lQh{hld)@V^zwMg_;k*64ehV2Vjd|H|MQn^HSTOPTZ@tj{Q&+tp!6MCm0Jn-b~We^XH5U~KhCVLXB&X%gMcAhEU*=)Lwx7*C^?KUfTySZXt<?FIEB5UF<wvwM2J~uzJZ!5+~0Xg_wwgI+1$S_(a6<6Xv;FqUijyFZ&7t8cX<4R}d$Kl9Y=n#CpK?TSrSq=1o6~(o9jQou~sQ>)GT_Y>wAn_);y+5q(j2SzwF;>*J<_y3q2a6%B5<cS_wem3Nl95q0)@=XsC_BW2+aQpcszn*O#n61q^4s9~6@2FDy7dG(_oao!k_(pA1_Z<ShKYqO*#On#3XY@px!4Eu1g$$eSpTs^HN`nfH_gS@6%E$GN{0f0<SbE{mt6e>&2DYZ0@&4jB@k9|)>Pvx0bkM~QK!aPdWi~3Y3w4^S74OsjkSKL#bC4LJrlCRJ53W%A4BgPgD+>oKVA>Ngda|ld`*!-;6@BeiNGe$aGIYRmVz5C>J{u+p5Q$C&Z}*ZcXbV=#*MZ(?5n-GtiqN;i+}mM|IGH_m2whQ<!~6n&xDZI*fNC8s*hR=?&$pIfARp!-+e9?T*RarP@_*O93bw<(*B&nS8~T~`RY5pwtxBW|3~i!{sk*Ep3(VOhy4%#wRe(ua~&LBorhDcNP#J~THaGM1)gFGtsgO-9px<s#Q?}TpbMAiaDxVehu+J15B@z1`(c)Oc$pM7IAJXAlBUTdGd!$bs5pv@ZLy|{pr>blsTl#$f*zGA=eIm2%ViTFo8na6#?W0G13Ni4!odL<Rx|+%Bbc*(D&JkNyk0v?3<ACP84;?5`iqWLtjmgZON%u}T_}0qD$086^Io?y^sL6P$e59o?mN7|bK2T)5-w;i#+b#;D&FPAyQRgc6c#5u#;yY`F31$;^WM{BK{?m7Xn5nKa0Lgq>zDB1%D#e=hR4w~t0w%SiPI2D<8*CendSfr70!-^lOVqfCMsZK`EYv|6d%InZLqX)jOV?(AOUb2LrNY3Yhy@hYTHO|!#gztzzZEoCgGh1hYHk8A0aWwz8vlX%k^616r#?r81FflP@$#K^Vz5u5Y`JA2iMs+7&4cl;>Tp(L!GVWm(3ei=Z9M#7-V(xIa^dCgJJiPRUGKx?KMkaKB&f#qW^A6hs8Dy#uMwIfuZ-2T^wj8a<RCcQhEsNAAnwSo?FpJ<OiSe(YnaBmyDgts^I#BEsUhsoL}}`NN};3Znr$`ZUd!@VP3@SLgF!omcI_Xr?3_0PO5U<fS!QfyK3b^AASVYmknN2iAw&$(ur*EW6d+Bu4@th)&B{)z?^wli3jp8)BIhG0{`v*;UP+bhu<%vRC7nuEog%%U9*b-srQf-)RG_2v(>+fh)A`gx8A?}7yma6`w{*AziP$irL*a)_3mE)q`B(Di`VO2z|e})v}1LyIO!!IpZ~SZ@-yMuZ=!wOD+FzXx5qGN#O(*RcM$gin(QUr%G7ZB%7=^BR|2-@$*02Y5RVhc8Zprx)V7f>j_unZSaV1yYeO?Ihh-3~IVx6Z;<;e;zz~eamVsk<^sFIzE(%IGJZqJnkNf5fVoh=k>L4KAFU2F%QU=8V0F189)*x^ii*-Cq0#mR(q%Yb!n(bBx*`#(8r1fSK#mzix_R}b5my~Pv&SM9*qvVk5T`-5-m*E8Ce&K#jw_Gh|t9GHxueZtkdYf^Q8&{k-0yB5dYL{VO)NBzgPwO?T;u=0PKtUQU3Gxb0<8@FY{JOZ!q;2cr$1)cFHA-RJ2X%w2^cc_dpEZv0`e&8N1z5TWcw;&SVAKf;kj5NZPnY=^YWq3huJWKnWb;Y>GjnB$29prh+#$Ri@8j|Gq!;u*cv%=sK@G?zOD|76ysqQ@?YWmF6HKadJ4S1WNUL+dkPN};yr8_NG<PG%J8^f}m(e9O_&p+t5&4{7q(0E^J=3A)nR+(vPDBD2e+fYNtpk0as66H+Zwaej8N1n3;H6s!0k;i^Li)=U5&hMTDZP2xt2ORW@hu|>7AuGWiW!yxeviU9v^bQgOFh<-4>j{97|6+sh3RG&4H{m)$cqt3nMA5uQ=)-!OdcA?o}n#)p%Ohtuq9X7Uu?8}E~!*bk%5jyzwloEaI9N-=VVH(lAQn|WHqxx8Ve}Q<5dU{rW`|mA_B1Bn2|~*hl-CIjhPN{8>BIPWk2@BnCU!l!6G4+Ax4?SzFkulepwwFAiY9B?HyLEAG<PoqPdd)G+n(dVv^MlD6lV~ZIv9mv9B-joZwi4_`PNo61=RAd)y840`v1Anm&er;AU!^jKy3ozC#fZn;{L+Fjt5`khFLZ&M25%50exy#l9Uz;>3w3HSu85kachfZvu94Ktm8LwDK%ckfYXst|UR>Vg>vI_m!pC0^5(nHj5TwC_2dp-;yi&IGtxJE$G++23b&C6oP^oESTU3=>k@DmleAfFzOgtqH|dZv1n7881Ks(U^P=D==jB}y%m1LO0HA>&|V0;Up&tGmQZPOQEOUJ_u&2c7^cZJb4PY0Rjz8wI80F$@8O33vuYjpYUOv9*1^IZqpye4yrzfeYr#@A3Hm_)UxvXa2OE|E_Yl@WSy{5}S4T<0uwC<MY+Rdtkwyb!atv;o;Vf$gYEqVkVA177!z+WrYd@|%0t#NfN3f<RZ$Yov0><hI3oBM^gd5Mu(UW2n8nZLJsdP0X=%a{ij<H(b(bh@gpcTeRg6-Hfi@1Evjt$FY>pg30XE64PU7psI&yelpZ?W!{(6^WQlnGx=DQi=Z0<8_O?Y$;%o@?bGHJuj82*|XIN+Kc;Yu_3Xd8l=$Ra2WB0eDQ@CEHb(aJSl-cdccQIj)bo*Kv`$Cx8B@sRKtkn_5^{*rmc^hc=o&{}V0u8Zb+)MJ#p`PLe(-;y}{t%-19V@AkvYVz1<8thwI7CWW1(BXgr4F-dC2k_nB5lF(-O*Q({u|H#fc5m`2$p<0?<$6+`iN?XU8=Nv#BYr-=;hOSdh4hs4~7>Z-f*U?RicXk_|yS6eBv&OjI!iEu>B@AqUpY9$^DNgq_e!iY0$&B_BTa3OIZxRZ4^<tSO5k=aXh3Q}Z0bNiN?Y%=z-Hzzw_CG;{h0KE7>;?@AL1s^JvwwX{Zl>2XR$Y+$)SQvv6^UZI0tM~kuHgyhV?=sVcbg-EXG_b%&G2EG220oq(_cbH7KkBCZiWk{HH?At0|ri{1U)<Lt3vO46qZbD=x~O?5Sj0$?2r7^xzZ-}j0NV%u6rSKxns##D=bo)<^ENc&BM$?oyge8;@fAd_dg7<3H#REh_1uSYqlr;M!)~5ZSVNqw}|fSnpDPJEi3Jd<N@rFd!j%`)jMuf;7?V-DY35V=#*qzKrqb%SZxq*blPB$|6G_zku*0o>uwW|NfPD4yAr3Eb<qcknR_1UMKj97sYjc%eGAysyFd)mEwOr(S6>Md+y5J7t%X$zp2L(|IcVbvLhf~Pi&>O2>xM~HLrD-4ZgX#nDzW~yRxn@4&uovX7r-}2ufpcouO^9-OwhrQW;m|LVU`7>@LIl@<;>X7P!AfIe8J#rHQ#m5PcnEgn}NJM8b^}>Y-?}Ux_lwLNS>$3^c)qRJ6r((DZ*3`(~NWTrPiBJU2C{8Q)Y{5kH#OqO0|^2)7a$QSm~HppV=u0`H#lHh$sqM_(Lr&&_cW&^r0Ed^Mtu-5fnax^e0cSYkFN;1~xEZstQ4;hS6xALNWTH%29)|aMCoa@>J5WT>DlZun0SEWu6)23foW)!183=(L`Pj{U5Xv+TnM38Gib#6*JGf9UU`DHZhc}qd2}UFRPBG^`h1(wu?eE$|ikSM%xPNP#HlRg07|v!E1D(A}gt)l~Od(i<VG?%31WFVrA5@FKMlaZDdNBY49OrQKP;GnxEgGdWTQ!N^w!z*msT%XyXPFJA;;{hkY46FoP9htgZ4Cu_ss8vr+CVX(6D$`Ib`kEIJ3Z-I}+AKiy8vTXYX<oh^9AznvP->UJQrmhl%&ia7}&t?e4!?YFEYs(P1YL^WZSOqSFPy6BieQySe4#xv^dc)Ja30A4{l;LbI&F~UY>H)cy~3=gS7KA+!wo84f#V*=ak);yNen*GMKl~0q!L9GqD(#<aXUynHP&9{9@`{eZ(j3WId{M~{5(n0MJ^qx16r;ozyQJ6f6CsJEUy&d@q^MeJbhru|swmnW*cQd+OtXONvw$+eFj~kd`3NuXEE#Ya{9OLM0N!R04l`Ua|r`q)pNXv+BPXyRGh8dd+M=*6pNxH0~>O%P+bJTZoJ*=F3$yg^qOTQREbvxMsInTmWfr_OJYieCb*$<gqJVes_T-V0{s?S@;wGNj)rp-Yr!ea(tWLWj6*#*BVdB11OQmZ3qe7ufg6)evi<(9P*nhKhIe=;ASdk}*yyham@^8*N%zP^31>Q}<Ts$P8H7|oXz==8~7K&d`jXw`>O)M?U7(5858G}r7b!MLcv%HXYuilJP2dcUs=7{Q-*+&XlN<}n1(`e|vKm=?Es@5feytcj5Nz};s>%_D5~uCVbl&V8pnyr+xTKr3!;G7T7~6>odlT?B@$g?Fdx{MIsTR-#c{|K(Gohz9m|4eu9^Ps%-_n)k_frz9@42QS;_QT!`3$;4#0itXw@S)T09EV81uimMv5S38iP+7_3_u}VscaD4dbIq|<=8X2pPX$RKaC?l-7tz>mH@dIruX(B|-$f3K}vu3^`^OwiZatuR<JerDfmIpu+!srJ`&$xA9J3am&H;Cey?-Nh?olMO!P~T`eN>jZyx+>g_!WRvX_M)uKvW=F9cbN6dx{u%VCgO7%&B%B!cfRFaUR~U=rZp6--YdPV_S#wx)z~8Atc)whnJFL7r#%+Us;Cp|f)^_J<r5DKR*YX&L_7`ipjH(<jKk4Z^+^$@8#;sS%aih$S{8rDEcO%;#ESjY(yO=FBI~Uzmgz3`6r6)a`k59kpc9W8$E7`l#D5DBva`N1`Ni~PfALTT`4uPizx=2F4Oy1xg*mgy-l!{81w-B-oLK(1mKf^I^IW+*lPQUcIHeJMYW8y77{`IFt5|>edj|;bpfuIhj)Bs7=&0He<plJa4@Qua@WwPChBvJ&PiCiSG7Cm5ptxZmW3gyp^}k3kR!IF93bwW<x^_Kaje%J?*z<(2{p8z8yb24bv`*=3GgFP~s<m_Nw%Z&rQ<Qa9%f1m`N5!}{l$3pUek(n40&<aIfFoiS!^<$hHAt-Yy%39~G7y)wG^wtx8|F(BMz%2-*~mAKNMpvO^r=O*DNGx@+g>L?m>w$Y)zCxU?4`_?pK*qlkw6Fsu=<aa+dgKB!&Hfz$KLZOZ(e}*>HRLsJv5P#Hy!MfmR5W$y|Jr(P>sNAVJ^JAzE1`)X+((JqM5ror0xo|Q;ZHfFwML7*5bz!8?GL%qar2~H17yTFAXjd2B2fEitY1BNkOh;>%5OVUh1!EcRmK;g+I&~-hzmp_^j_bduv{!zL_=AmQi`TxL10Ay0`l7bg%s0G_RXqnwFh3Z80T7;~o~1j1(s7V*LMBcV)|M99Q&RU(rI!F2Eu{09-_gmQ)l;(TqilA)v^TY=Z+}NKOb~P{4qTs#ulEM>u}S59BQmdG<s6C;5`}y}e9tGw6ZHNOs8}Fw^Vp?e^UcJx3rUTLApfX{be|=ZYUerTqBwl9u8NKcWCn*oqGVwMugs{8cGb${;|gqX2Rko$A0EyfX(Z*uu-L@Ah7A?d`Vcz79G_PJr^2vZ-Iydcp@OEi~QPeLEL{xLvFMnf9}m`nu4gYmn$JGoli3H?0uur;CapVU<Ks#jPn7JbZVMlqw_$%T^Kjoi0i6j!x#+0Qzmqbf$bE<+^du5~?hr=77$#>X!fa#p7CxoVA2dQpc7Dlh%h<W~2uu-6$@}t1){?4;@&79XNZI`0!UM>RB$c3RRLaF_blk7E=(|95&9Vm&Tsvx5!!Y65@%@b7`UJs=-yHdE<+`6<JEAj*y$?0~Y4?EZL$3vDNwk^^X7j$KS|1C<L#T@arvM?&kCJZG(jec_(wS-){|DB3^)BS0Ql~UE7tuswGtP0-aM(q&P%$I{VoJQu+cKo${-%PEHKRbJ%!1mI&LfG%HV*u_B9bHW6QPC(~eZ&Pe*puZ)zx{8bkuaf|?NB%LF^!enSjT!l(Cx5Bgx3!rn7>S0+bG0&AudN0z5NaKmTt<&2%CNIf|3nk@lr<tqNx?#U_g{CRZdTI}nlla;<@i4gRd|*Z|(pbuDi?ouejp7d<SgZ}OjjFAhhFU|XAKQrT2wqG=)Yus1atK(`yqIm6D1#M%8uTmdxfWYeWVMW0&&@!%A|)4+rT52*Qi{0Bs`+nh0)5KhiXxmLkJZcq8uA~Rn<S)>;nU@hu@P)12WcRak^UGc7M2$-XU}mg%ovKZdD|0R6S3jjIxov4>}x^5=>2vE&e_aeTwaOc!k7fTb78K8;gS@WRZ4a{7nJSJWwG%Lot}65`D}V!?$QsPkB285#U7wBrq_$`@yw97AR8}ubESu(e(VVpki@|>X-AaRRzg;%U8EPzHl!%Slmr{r-N__nZal0^N?1X)8-R#VQ&)tBs=_)Z<-rG!D>9LN8400Hloya{KHf@K9$=$N7Z7qr$D~W?K+kTl6o&8dEKy&u)EdRWjF2aE$t|?1Cn2C=TeaUT0cu~}v9OQ;hs@t?5FQ0|HV=Uw(=hDQ!$Cz0oFaA_dk%-h4$Qn!d|9UZ;?t*3iH7(`8NPl-)MP9Nk17Z$P@a;XXt7vAW3948kG9qIjb?ML@d(bHmFD{T>c*o-jfYw#QUk_wB5vqv^U>;~^@q(zYXbgFvuGMeJ>8xum`s%04gK|Afh2_vlp(?;eJ(iZA2*E>=fxTxYjNbE0p<5hsk)RZGM9Aa<Bu}087=LJUS6u8eMVN8Q97%kS?7q!bq004x|WuihSU=6Y1ANXqlO<30fZSmxSKU4(@D?^JE*ePGS(RcRAZI?zn-Qxf<KDn_1XqjQI{VLrHbqT?FyKr%dks}A#Oxfe4=8^HUPv@j%s678zMae__43A>W0O7$zMt0DFg!?a3DF5u2L~tqy#__6G22=!LYZq5;haAlo_C#K&3gg<V!M~ijmO@9-?>l=@Zgi2X@<zCqjAeX-qkblBR98Y=#{B$ut;62~EO0;9E&JEThSu?kWvis1ng%u+4OpQSKo)4M+5fC*6XU-~aT(<qy>w`SHQ>=@PS)m_);}lH!Lcd(|=Y<E$dH=sQLBYu3o?eS&gl@+Lxz_AlYoNbVB3uN#f}ulI$7(%_AdDbTGr!wY)Qo{Vn6meZ24i=uUd&Uj=SbGpL1D;|L^={KJ+^wx-yWiE9P<}++ksIqZ(84D(4*BE|9whB#?93lp#W;%j#IH4@i5O_}B8IckhLp$YBh$;1?;y_i?yADMm6haP4*|pdfgr(rV^$7lhgR!xBZ;sMOts4q{jGquu9Z32(>*O*NLdBFKQrVHmR}{fCxkJf&%6CpU3)zt*>zAzf|2OVwBlP*Xqw7b+Ir^eMwmLhzFScI4Y<CW~j<yb3M#fAk+H#*K#K6auiU6S`(G|$OS(0xs1Z&$8S*hZ^ZgGj1l<(~_;hqwQzf><7X)uBe`<un$tFo=R6Kk&WC`WOl%@I|G>)P{h%j1wUQo*2aa007D%3a0W;}U+4jfI{M;gu!k--o9Q$@+=eVp;I}GOLU3Pyn2qR>*khAF*5weMOXcNi)Wm4y`Rfy9YMW)WZk_D~uyXhgN2L&D(}Si0Mrw1Qezjl6x48X2C!-9%4<)*PHfOh*xq)$l42p$|iR}G_hxn5EQvGWX152pnHZ!%9weS)7XjWbqD4yX$Re@9!hk6gk(_SoMS9eu!YDAhR;fKORD%w5D*kq#>=(>gP#`T3Zx%&nO!A@t(%r~X<ku<k?1#V82wbw64Ci{*7<Ws=g)ONvy=emxeCrS70!XQyG~CeCy;i!j8czyVZG4`E+A|Wv*jb(XVG}7Pg`tHbxM;7JOZyxr5ohR(3JA3-C$C(5HaTmKvPQ4?V2!bX5g>|ipL?ayZ7l!h2rS59*w5u61-O}0Q7WXWH8kd7G?;Cv3#)ERRg5qOC>~_&AP(uJP2om@`&^XJJCG-Am<4s!}M9L?1Jrb?=|SCG#M5jwU46vZ4A85%SS94T}r-Z%J;_}q!f&QCXHPe3Hal*q7im>2SGHNN2c^LV_42X<_a$)ds1i?Zh2-~Ku<cPkjFugq71!l$%RJC+Fb5~;vM*=4jAR7g1#jc3oD~JMv~4r@kteq=A;tFp^v%ah5Bv|0o?F%+4ep+<|d<W5<<qRZzZnlgff2Ch2lmxMBt7Fus7!)%zxkui)EM+ZiiRx(X4srv{HfltX2{%a$eh3;~;g=%XA#xy@2~lpyN&cY3u5Ob>ga3=AXKHO6FOwwKwDR&7L>b2`s^B2-n|`@-c{PkC(_X7yq)aQv7>d`Q$(^i*ah`qvQ(&qo1kwPm?sFk~7rNX=1}EE+UxF#PO$z-i*`404~vTn!<R9`BTpUkhO*PD^iYaAjsaW3}mi_p+039h|-^Cpe$hsBjw}zfBps2w6VtiuJGTh@Ec9H8&#YlWO^B)%ABxSPO4ASd5$x(v9`QYUtV3iU-?uRIVrr%V)LAh<-+hf{__?uFEG(i0pbf)jFWfMe^Tmm(vBtJ6%WmAK<<a6tgeK)t)-v8mlXu?V|3|E;1+*OmdWuTJV~_O{gXl!EjIbjKt)yn%E;K~X?Am;Pf?C=KAoN2(nhbAOH1ASOy^4LG8mJ04e~YJDc?1<3*MBzs-mXucBIQ(pwcj}BC1}~d1W$Gs@CGp$*QSVlZLOnI)4Om=$|d`_Yv39@nGlP0V>Ja@%QO4w^Y2W#g^;G;dL#z@>C0h;l<~n>M6D;ZG2qL4sm%}`FOwe3PCo1`#bPKtz_0ks7&_r8=3`iqae670AJF_l~0FAnxbqjHi;I;GA+jI7|^6S43A}C0<_QMc?{56Oy0~+ZUGQuhLw%X3>G*s<Eqx2zDovdYLQODOe)mLm3qNWHrI=Gay^%KoY$Xv{f-B%{xSXe961Ky4XkiibL=RJ>z>_KR>Ja8>Lz&@FJCQm4iP*L=R;&f$X<h7Oqpn9ugO6EK*Pn5{Zg<#!AF^}dS2=|1J=&~^~<$?HkGtGDBohWV^+_)Rm)$x+dwITF4-t_&{zmsW#P#2Xk2sV*kY^#;@xTHZMxpu+mkl8uAGINL&@7&w&{vB;q2~|q$)a^$HM(&gpje=?vNG+%G>8e4s*fjLFVqBCQwn%qPweZYBBNdu$Q*^YgSM1e7w2UxVayjKz#Ol4Tw*iDC_kNuft@4lixBp=BCDT689r|^#c2Cy!CC=>e=b7^_W_3=OouFXf|uj`B}oTuveEx-49c!vfzqAm1+5PL-#6Jc2_DNFP8A+ZzSXmy?YKo$L;_hzVN<0`ncs^<lGxC7QQ!{wsRMGSI5+YAC!Qmm7RnCg%v<EorOU%490#86;BL?A=-mY3xqe<BTT8*5UUNCcsdgdh2^T!WT7e-MGbR>bo11dT7$Kmw6qG;?8q(rf3mVWZHO!z6WU+In3?)f8C2jeFnvns^jUFQ^ST$HR$6QE9$!WiPa8f+c`{)JCHIX-#e0kOF3?w5rOXRpC~PyrATHq*2%_kn?u>5LeFEtTEIn`x=!e5#)L#Nfxe#0xqJ$yMokeh6ug%-q)ZL3o-xML)VK@QbQQFu5#A5Au9FsCP#E0I;6?jZ{(oqr&Nco%J{t5Ot`0xnI(1d2aVCcK?(WJSX9xp1xx0b#9XmOcRj??O4SjrTCMbo&1Ho-{H+I0YS+0}aOVRKVFLwF1nS*)#Zx<sFf_`)H3O5(Aj20RxJ_sLgKtW{N`w)${^s!m{d3s+XJ)i)NXjLRQyi*~kT_#Ig$Z^<@Vs<(KIlI=k>9>dys9!yfJZ#7zl*Jh%JmzWcC;u`IOKbY_e-NF$x_(1~3^MmeZ7&*gd-`0H(D6#1S{F38Vq&q{<J$5+WA0?LEeI5Tb>ZX0*U}1NL3{pE<^@O1n8SV=L@6Qp(qu@~oQ{gNaoD`d$j9~8Ou0eaj4Rx(v*wi=Ed1P@?qls>0BNtnZzwH4kt<}FM`3(l$Qw}0pYSjs^?v!UrsB}M`OyZ&|Jeho^U!o|dk-Pv-;$W(J2<6_6{pOm$KKE)ezl#~D=eaKxNc0~3eT+YEsRJrHy5H`iG!o#g_y+T05C`@aqc}u^nU80id-0IABK%gO+k!JlJR659bbu;}Haa1tE{?0IIycczhU|otX$wiKH<@(_!zdtM0;ktQJX^Z3!m(oESZy%-FnaDb*|!JjH+WaEnuSI_p48Q*G;*V65Zu#zlGlOS__4CC(p>uDBthdS=remG%AxG+?lq6LcJ!gyf)*czK|h`)8eqdm%{Ku98+u>!k#beYk<0XoBHdiCc)PgaZ}y-lQCgE=N41_)YjrTmY0sE&zz%h(4pq5qK6{W>DaR08(%NrcbtvcgfPYCJnF7I_A@-0NdOGR61i0>PjDAqv;n5GsD~x_X$~(}3PEZkxE~0BKJt!!{sp5IlA=nA#x^}=$45d~BEu<XeRptZybj$>V%Lpg^_!9JJ-S9LTfq-$3_H;H;<Xsura~C)9goN~1+tmh($WSlpY3#sXDX`zFf^T8fKZ>SjI4W6p#^EqZ6dL-Qt!(;@)ohHW?yMbiM<|uX>p5;5=Q++IFUKR8VR+#Sy1KG1dz33+U>#Q1Omn~mWZGV#MZApCoYTX5a(GICn>z$ElXr1EM5Xp%K>HdhEBym~<9j{~psXt7$UPrKk?!+Byj}c!z-C~N<o2%?>e&9%hO_OzQF~Z;f0d5XSXPfy(vJ<rJc9WBlzY~n>+5|SjOK)P#D-up%c;&I45{7??cRcAR#*!hLPL?MpGJh$`k@ORA!=hcE3Bzb7r4j&{BL%D|M^${YYz($L)t7v^q1ryguMrh!{M;&(Zg;Fj9j)6kL{kSOEmG<io_8y0#lPD-ad=L3(!1AN{H_{4Iy8GRQvPR%l)0s?)QhUj@q5}*3sT>yOj+aUL*qc{P@?o(XYo4SXDQ|&(THQ6tE)E&5Z<7UJ-gbG4<vv;WewDNi+;5*W}ft7x0;Jh&`s0hEF0E`c74ou~>G`Z!hv)TA+J}Oy4gqIu1~_qL<|2i!p&IKMr~VvxzRb4%lzm(}K9;2`aG|G8|Gh?+)&qYSgo&rO~GU<D509XY+OBBrenfSJzB!z3!=5QsxvK{G>aH=t3Z)7%+=QBMga8$}PaP3ZOY~=LKzLrB>2HSXh_^>3Wsp!n?gPJVD?o^Z7Ix7-Pj*$RVE;b}4l0#lJ8ZiSARw^Kx%zM^G-y*A|1k*1%4K*0^~$Q-(Jl%nFV90`ZdqI#Fod|Bs1eR8HH&yqS?;zw22BPRX5<c+ht&ecQntQ!_G7MJ~-tI$IU8H;B9Rto}B<?#2KD)jFev^yo$TF=>s19!xtB2rM54vnf4Kx0A`>!8`g8n0Nm3Em>w?T3}*|Zy|=39!%ceO3%Y<egSo!KO%4l2pZ)1!a~6CvxdI=4rlx`E1;NorN?bo;PZGSPbeM8z5m_e>o%@u`KZ17J>?E|xAdp2-Iu%D?UH$&VZm!;sGSm$P8&G%sRjb<geSplkd&=Et)GZ@j*xd@fkrw9p(AuO>5PD$hcy69qCYB(_H@*AfJ31P^6e}m6<Q->sY=u}H5oQXiQRU4O}+MRs<UY~icD6Inb?hEx+%~4Q4A50{jnvW?e{Y-4EjXl-g|WIw|U&5ewfgG2X=$~(O+-}!Z&3_CM1(rjF?68g^0Cy3Tt!1V*9swsQ(CqG;_N)WJdAw{06qZM81jW!Sp8V?!6QYa9J^hQzII(r@6t8a_zGUqJR*wGsE8f9QSJ_EVVvhoA+)i@cH#JLp6I!zk$&={5?yCgQxfY2e1O7H~')).decode('utf-8')


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
        "languages": LANGUAGE_METADATA,
        "initial_context": ctx,
        "fallback_params": fallback_params,
        "fallback_presets": fallback_presets,
    }

    html = _STUDIO_UI_HTML_TEMPLATE
    html = html.replace("__INITIAL_LANG__", norm_lang)
    html = html.replace("__INITIAL_DIR__", LANGUAGE_PACKS[norm_lang]["direction"])
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
