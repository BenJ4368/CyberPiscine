# CyberPiscine #4: 🧩 Reverse Engineering

> Projet de cybersécurité 42 : Desassembler des binaires pour comprendre leurs fonctionnement.

## Level 1️⃣

Avant toute chose, lancons le binaire ! <br>
`./binary/level1` <br>
Un simple prompt, une entree utilisateur et tres probablement un comparaison de cette entree avec un mot de passe.
- - -

Essayons d'en apprendre plus : <br>
Utilisons un outils 'simple': le debugger `GDB`. <br>
Lancons-le en lui donnant le binaire; `gdb binary/level1`. <br>
La commande `info functions` nous liste toutes les fonctions appelees par le binaire. On y vois entre autres: <br>

- `printf()` le prompt.
- `scanf()` l'entree utilisateur.
- `strcmp()` la comparaison.

Creusons plus loin: <br>
Adaptons d'abord la syntax qu'utilise GDB, pour plus de lisibilite avec `set disassembly-flavor intel`. <br>
Ensuite, desassemblons le main() avec `disassemble main`. <br>

On obtiens le dump assembly suivant :

```
   Dump of assembler code for function main:
   0x565561c0 <+0>:	   push   ebp
   0x565561c1 <+1>:	   mov    ebp,esp
   0x565561c3 <+3>:  	push   ebx
   0x565561c4 <+4>:	   sub    esp,0x84
   0x565561ca <+10>:	   call   0x565561cf <main+15>            // start main()
   0x565561cf <+15>:	   pop    ebx
   0x565561d0 <+16>:	   add    ebx,0x2e31
   0x565561d6 <+22>:	   mov    DWORD PTR [ebp-0x80],ebx
   0x565561d9 <+25>:	   mov    DWORD PTR [ebp-0x8],0x0
   0x565561e0 <+32>:	   mov    eax,DWORD PTR [ebx-0x1ff8]
   0x565561e6 <+38>:	   mov    DWORD PTR [ebp-0x7a],eax
   0x565561e9 <+41>:	   mov    eax,DWORD PTR [ebx-0x1ff4]
   0x565561ef <+47>:	   mov    DWORD PTR [ebp-0x76],eax
   0x565561f2 <+50>:	   mov    eax,DWORD PTR [ebx-0x1ff0]
   0x565561f8 <+56>:	   mov    DWORD PTR [ebp-0x72],eax
   0x565561fb <+59>:	   mov    ax,WORD PTR [ebx-0x1fec]
   0x56556202 <+66>:	   mov    WORD PTR [ebp-0x6e],ax
   0x56556206 <+70>:	   lea    eax,[ebx-0x1fea]
   0x5655620c <+76>:	   mov    DWORD PTR [esp],eax
   0x5655620f <+79>:	   call   0x56556060 <printf@plt>          // printf()
   0x56556214 <+84>:	   mov    ebx,DWORD PTR [ebp-0x80]
   0x56556217 <+87>:	   lea    eax,[ebp-0x6c]
   0x5655621a <+90>:	   lea    ecx,[ebx-0x1fd7]
   0x56556220 <+96>:	   mov    DWORD PTR [esp],ecx
   0x56556223 <+99>:	   mov    DWORD PTR [esp+0x4],eax
   0x56556227 <+103>:	call   0x56556070 <__isoc99_scanf@plt>  // scanf()
   0x5655622c <+108>:	mov    ebx,DWORD PTR [ebp-0x80]
   0x5655622f <+111>:	lea    ecx,[ebp-0x6c]
   0x56556232 <+114>:	lea    edx,[ebp-0x7a]
   0x56556235 <+117>:	mov    eax,esp
   0x56556237 <+119>:	mov    DWORD PTR [eax+0x4],edx
   0x5655623a <+122>:	mov    DWORD PTR [eax],ecx
   0x5655623c <+124>:	call   0x56556040 <strcmp@plt>          // strcmp()
   0x56556241 <+129>:	cmp    eax,0x0                          // cmp
   0x56556244 <+132>:	jne    0x56556260 <main+160>            // jump to main+160 if cmp !=
   0x5655624a <+138>:	mov    ebx,DWORD PTR [ebp-0x80]
   0x5655624d <+141>:	lea    eax,[ebx-0x1fd4]
   0x56556253 <+147>:	mov    DWORD PTR [esp],eax
   0x56556256 <+150>:	call   0x56556060 <printf@plt>          // printf()
   0x5655625b <+155>:	jmp    0x56556271 <main+177>            // jump to main+117
   0x56556260 <+160>:	mov    ebx,DWORD PTR [ebp-0x80]
   0x56556263 <+163>:	lea    eax,[ebx-0x1fc9]
   0x56556269 <+169>:	mov    DWORD PTR [esp],eax
   0x5655626c <+172>:	call   0x56556060 <printf@plt>         // printf()
   0x56556271 <+177>:	xor    eax,eax
   0x56556273 <+179>:	add    esp,0x84
   0x56556279 <+185>:	pop    ebx
   0x5655627a <+186>:	pop    ebp
   0x5655627b <+187>:	ret
```

### Analysons un exemple pour mieux comprendre:
`0x56556227 <+103>:	call   0x56556070 <__isoc99_scanf@plt>`
- `0x56556227`: addresse memoire de l'instruction
- `<+103>`: offset en octet depuis le debut de la fonction (ici, on est 103 octets apres le debut de main)
- `call`: nom de l'instruction (ici un appel a une fonction)
- `0x56556070`: adresse memoire de la fonction appelee
- `<__isoc99_scanf@plt>`: nom de la fonction appelee. Ici, scanf().

On cherche a connaitre les valeurs comparees dans `strcmp()`, puisqu'il est tres probable que le binaire compare l'entree utilisateur au mot de passe que nous recherchons.<br>
`GDB` nous permet de suivre et controler l'execution du binaire en placant des breakpoints.<br>
Ici, on veux placer un breakpoints dans `strcmp()`. On fait donc `b strcmp`.<br>
Une fois nos/notre breakpoint place, on lance l'execution avec `run` (puis des `next`, si besoin).<br>
Lorsque le binaire nous demande une entree, on y rentre une valeur reconaissable. Par exemple: "CHEESECAKE".<br>
Une fois sur le breakpoints, on souhaite afficher les donnees stockees dans les registres avec `info register`.
Google me dit que `strcmp()` utilise les registre `ecx` et `edx`, affichons donc les donnees de ces deux registres avec `x/s $ecx` et `x/s $edx`.<br>
L'un est notre valeur reconaissable "CHEESECAKE", l'autre est le mot de passe.<br>
On peux sortir de GDB, pour lancer le binaire et tester le mot de passe.


### level2

On test `strings level2`; On vois plein de trucs. Du lorem ipsum pour noyer les infos, `memset`, `atoi` et d'autres. On note aussi le mot `delabere`, tres etrange. On essaie aussi `objdump`, comme pour le level1 mais GDB seras plus efficace ici.<br><br>

On desassemble le main dans GDB, et on s'appercois qu'on a des appels a des fonctions dont `no`, `flush`, on retrouve `memset` et `atoi`, mais aussi `strlen` et `strcmp`. Tout en bas, on vois un appel a `ok`, apres `strcmp`. Je suppose que c'est cette fonction qu'on cherche a executer.<br><br>

```
   0x000012d0 <+0>:	   push   ebp
   0x000012d1 <+1>:	   mov    ebp,esp
   0x000012d3 <+3>:	   push   ebx
   0x000012d4 <+4>:	   sub    esp,0x54
   0x000012d7 <+7>:	   call   0x12dc <main+12>                // start main()
   0x000012dc <+12>:	   pop    ebx
   0x000012dd <+13>:	   add    ebx,0x5d24
   0x000012e3 <+19>:	   mov    DWORD PTR [ebp-0x40],ebx
   0x000012e6 <+22>:	   mov    DWORD PTR [ebp-0x8],0x0
   0x000012ed <+29>:	   lea    eax,[ebx-0x42e5]
   0x000012f3 <+35>:	   mov    DWORD PTR [esp],eax
   0x000012f6 <+38>:	   call   0x1060 <printf@plt>             A// printf()
   0x000012fb <+43>:	   mov    ebx,DWORD PTR [ebp-0x40]       
   0x000012fe <+46>:	   lea    eax,[ebp-0x35]
   0x00001301 <+49>:	   lea    ecx,[ebx-0x42d2]
   0x00001307 <+55>:	   mov    DWORD PTR [esp],ecx
   0x0000130a <+58>:	   mov    DWORD PTR [esp+0x4],eax
   0x0000130e <+62>:	   call   0x10c0 <__isoc99_scanf@plt>     A// scanf()
   0x00001313 <+67>:	   mov    DWORD PTR [ebp-0xc],eax         A// save eax into ebp-0xc
   0x00001316 <+70>:	   mov    eax,0x1                         A// save `1` into eax
   0x0000131b <+75>:	   cmp    eax,DWORD PTR [ebp-0xc]         A// cmp (eax = ebpc (=1) ?)
   0x0000131e <+78>:	   je     0x132c <main+92>                A// jump to main+92 if cmp =
   0x00001324 <+84>:	   mov    ebx,DWORD PTR [ebp-0x40]
   0x00001327 <+87>:	   call   0x1220 <no>                     A// no()
   0x0000132c <+92>:	   movsx  ecx,BYTE PTR [ebp-0x34]         B// save ebp34 into ecx
   0x00001330 <+96>:	   mov    eax,0x30                        B// save 0x30 (48 ascii, so "0") into eax
   0x00001335 <+101>:	cmp    eax,ecx                         B// cmp (eax = ecx (="0") ?)
   0x00001337 <+103>:	je     0x1345 <main+117>               B// jump to main+117 if cmp =
   0x0000133d <+109>:	mov    ebx,DWORD PTR [ebp-0x40]
   0x00001340 <+112>:	call   0x1220 <no>                     B// no()
   0x00001345 <+117>:	movsx  ecx,BYTE PTR [ebp-0x35]         B// save ebp35 into ecx
   0x00001349 <+121>:	mov    eax,0x30                        B// save 0x30 (48 ascii, so "0") into eax
   0x0000134e <+126>:	cmp    eax,ecx                         B// cmp (eax = ecx (="0") ?)
   0x00001350 <+128>:	je     0x135e <main+142>               B// jump to main+142 if cmp =
   0x00001356 <+134>:	mov    ebx,DWORD PTR [ebp-0x40]
   0x00001359 <+137>:	call   0x1220 <no>                     B// no()
   0x0000135e <+142>:	mov    ebx,DWORD PTR [ebp-0x40]
   0x00001361 <+145>:	mov    eax,DWORD PTR [ebx-0xc]
   0x00001367 <+151>:	mov    eax,DWORD PTR [eax]
   0x00001369 <+153>:	mov    ecx,DWORD PTR [ebx-0xc]
   0x0000136f <+159>:	mov    DWORD PTR [esp],eax
   0x00001372 <+162>:	call   0x1070 <fflush@plt>             ?// flush()
   0x00001377 <+167>:	mov    ebx,DWORD PTR [ebp-0x40]
   0x0000137a <+170>:	lea    eax,[ebp-0x1d]
   0x0000137d <+173>:	xor    ecx,ecx
   0x0000137f <+175>:	mov    DWORD PTR [esp],eax
   0x00001382 <+178>:	mov    DWORD PTR [esp+0x4],0x0
   0x0000138a <+186>:	mov    DWORD PTR [esp+0x8],0x9
   0x00001392 <+194>:	call   0x10b0 <memset@plt>             ?// memset()
   0x00001397 <+199>:	mov    BYTE PTR [ebp-0x1d],0x64        ?// 0x64 is the letter d
   0x0000139b <+203>:	mov    BYTE PTR [ebp-0x36],0x0
   0x0000139f <+207>:	mov    DWORD PTR [ebp-0x14],0x2
   0x000013a6 <+214>:	mov    DWORD PTR [ebp-0x10],0x1
   0x000013ad <+221>:	mov    ebx,DWORD PTR [ebp-0x40]
   0x000013b0 <+224>:	lea    ecx,[ebp-0x1d]
   0x000013b3 <+227>:	mov    eax,esp
   0x000013b5 <+229>:	mov    DWORD PTR [eax],ecx
   0x000013b7 <+231>:	call   0x10a0 <strlen@plt>             C// strlen()
   0x000013bc <+236>:	mov    ecx,eax                         C// save eax into ecx
   0x000013be <+238>:	xor    eax,eax                         C// eax XOR eax (puts eax to 0)
   0x000013c0 <+240>:	cmp    ecx,0x8                         C// cmp (ecx = 8 ?)
   0x000013c3 <+243>:	mov    BYTE PTR [ebp-0x41],al
   0x000013c6 <+246>:	jae    0x13ee <main+286>               C// jump to main+286 if cmp >=
   0x000013cc <+252>:	mov    ebx,DWORD PTR [ebp-0x40]
   0x000013cf <+255>:	mov    eax,DWORD PTR [ebp-0x14]
   0x000013d2 <+258>:	mov    DWORD PTR [ebp-0x48],eax
   0x000013d5 <+261>:	lea    ecx,[ebp-0x35]
   0x000013d8 <+264>:	mov    eax,esp
   0x000013da <+266>:	mov    DWORD PTR [eax],ecx
   0x000013dc <+268>:	call   0x10a0 <strlen@plt>             D// strlen()
   0x000013e1 <+273>:	mov    ecx,eax                         D// save eax (strlen() output) into ecx
   0x000013e3 <+275>:	mov    eax,DWORD PTR [ebp-0x48]        D// save ebp48 (=2) into eax
   0x000013e6 <+278>:	cmp    eax,ecx                         D// cmp (eax = ecx ? so strlen() == 2 ?)
   0x000013e8 <+280>:	setb   al                              
   0x000013eb <+283>:	mov    BYTE PTR [ebp-0x41],al
   0x000013ee <+286>:	mov    al,BYTE PTR [ebp-0x41]
   0x000013f1 <+289>:	test   al,0x1                          D// AND operation on `al`, weakest bit of eax (is eax even/odd ?)
   0x000013f3 <+291>:	jne    0x13fe <main+302>               E// jump to main+302 if cmp != (continue while loop)
   0x000013f9 <+297>:	jmp    0x144a <main+378>               E// jump to main+378 (break while loop)
   0x000013fe <+302>:	mov    ebx,DWORD PTR [ebp-0x40]        
   0x00001401 <+305>:	mov    eax,DWORD PTR [ebp-0x14]
   0x00001404 <+308>:	mov    al,BYTE PTR [ebp+eax*1-0x35]
   0x00001408 <+312>:	mov    BYTE PTR [ebp-0x39],al
   0x0000140b <+315>:	mov    eax,DWORD PTR [ebp-0x14]
   0x0000140e <+318>:	mov    al,BYTE PTR [ebp+eax*1-0x34]
   0x00001412 <+322>:	mov    BYTE PTR [ebp-0x38],al
   0x00001415 <+325>:	mov    eax,DWORD PTR [ebp-0x14]
   0x00001418 <+328>:	mov    al,BYTE PTR [ebp+eax*1-0x33]
   0x0000141c <+332>:	mov    BYTE PTR [ebp-0x37],al
   0x0000141f <+335>:	lea    eax,[ebp-0x39]
   0x00001422 <+338>:	mov    DWORD PTR [esp],eax
   0x00001425 <+341>:	call   0x10d0 <atoi@plt>               E// atoi()
   0x0000142a <+346>:	mov    cl,al
   0x0000142c <+348>:	mov    eax,DWORD PTR [ebp-0x10]
   0x0000142f <+351>:	mov    BYTE PTR [ebp+eax*1-0x1d],cl
   0x00001433 <+355>:	mov    eax,DWORD PTR [ebp-0x14]
   0x00001436 <+358>:	add    eax,0x3
   0x00001439 <+361>:	mov    DWORD PTR [ebp-0x14],eax
   0x0000143c <+364>:	mov    eax,DWORD PTR [ebp-0x10]
   0x0000143f <+367>:	add    eax,0x1
   0x00001442 <+370>:	mov    DWORD PTR [ebp-0x10],eax
   0x00001445 <+373>:	jmp    0x13ad <main+221>               E// jump to main+221 (restart the while loop)
   0x0000144a <+378>:	mov    ebx,DWORD PTR [ebp-0x40]
   0x0000144d <+381>:	mov    eax,DWORD PTR [ebp-0x10]
   0x00001450 <+384>:	mov    BYTE PTR [ebp+eax*1-0x1d],0x0
   0x00001455 <+389>:	lea    ecx,[ebp-0x1d]
   0x00001458 <+392>:	lea    edx,[ebx-0x42cd]
   0x0000145e <+398>:	mov    eax,esp
   0x00001460 <+400>:	mov    DWORD PTR [eax+0x4],edx
   0x00001463 <+403>:	mov    DWORD PTR [eax],ecx
   0x00001465 <+405>:	call   0x1040 <strcmp@plt>             F// strcmp()
   0x0000146a <+410>:	cmp    eax,0x0                         F// cmp (strcmp = 0 ?)
   0x0000146d <+413>:	jne    0x1480 <main+432>               F// jump to main+432 if cmp !=
   0x00001473 <+419>:	mov    ebx,DWORD PTR [ebp-0x40]
   0x00001476 <+422>:	call   0x12a0 <ok>                     F// ok()
   0x0000147b <+427>:	jmp    0x1488 <main+440>               F// jump to main+440
   0x00001480 <+432>:	mov    ebx,DWORD PTR [ebp-0x40]
   0x00001483 <+435>:	call   0x1220 <no>                     F// no()
   0x00001488 <+440>:	xor    eax,eax
   0x0000148a <+442>:	add    esp,0x54
   0x0000148d <+445>:	pop    ebx
   0x0000148e <+446>:	pop    ebp
   0x0000148f <+447>:	ret    
```

On va approfondir quelques trucs ici;
   - les 'registres' sont des moyen rapide mais temporaires de stocker des donnes utiliser par le CPU pendant ses calculs, ces registres sont souvent ecrases par les appels de fonction suivant. (eax, ebx, ecx, edx...).
   - Pour les faire persister (le temps de la fonction), on deplace le contenu de ces registres dans la memoire. (dans `ebp-0x35`, 'ebp' veux dire que s'est une variable locale de la fonction actuel, et '0x35' est un offset qui indique ou est stocker cette variable par rapport a 'ebp').
   - Ensuite, voyons quelques instructions utile dans notre cas:
      - On sait que `call`, appel des fonctions.
      - `mov` (mov a,b) deplace la valeur de b dans a.
      - `movsx` mov, avec une conversion en entier signe 32bits si necessaire. (pour les caracteres ascii par exemple)
      - `cmp` compare deux valeurs.
      - `je` "Jump if Equal", saute vers la destination si la comparaison est egal.
      - `jne` "Jump if Not Equal" ...
      - `jae` saute si superieur ou egal.
      - `jmp` saute vers destination.


Avec ca, on peux deja essayer de deviner la structure logique;
   - block A// On prompt une entree utilisateur avec printf()  et scanf(), et on compare la sortie de scanf() a 1 pour verifier si la fonction a bien recuperer une entree. Si non, on call no().
   - block B// On verifie que les deux premiers caracters du buffer rempli par scanf() sont deux caracters "0". Si non, on call no(). Appelons le buffer de scanf() "password".
   - block C// On verifie que `strlen()` >= 8. (strlen(password) probablement)
   - block D// On verifie si `strlen()` est pair ou impair (La je sais pas trop ?).
   - block E// Ces instructions sont tres probablement celles d'une boucles while. C// et D// sont probablement des conditions de cette boucle. On vois un AtoI dans cette boucle, et tout les `mov` qui le precede font penser a la creation d'une chaine de 3 caracters. (merci gpt la)
   - block F// Ici, enfin, on a le strcmp finale qui nous dirigeras vers `ok()` ou `no()` une derniere fois.


Avec tout ca et pour la faire courte;
   - On soupconne que la clef et `delabere`, parce qu'il est louche, et on sait que le programme place la lettre `d` avec `memset()` ligne main+199.
   - On sait que le programme veux un password qui commence par `00`.
   - On sait que le programme creer des chaine de 3 caracteres de long, et les passe a AtoI().
   - Donc, on cherche un mot de passe qui commence par `00`, et qui transmet ensuite a AtoI() les 7 lettre `elabere`, sous forme de packet de 3. (Donc on doit avoir un buffer de 2 + 7*3 = 23, + 1 pour le `\0`.)
   - On oublie pas de caster la sortie de AtoI() en char pour que les groupes de 3 chiffres nous donnes les lettres souhaitees.

Ca nous fait:  `00101108097098101114101`
   - `00` qui sont demandes.
   - `d` qui est donne.
   - (char)atoi(`101`) = `e`
   - (char)atoi(`108`) = `l`
   - (char)atoi(`097`) = `a`
   - (char)atoi(`098`) = `b`
   - (char)atoi(`101`) = `e`
   - (char)atoi(`114`) = `r`
   - (char)atoi(`101`) = `e`

### level3

Pour ce level3, on arrive sur des trucs plus complexe.
On va utiliser mieux que gdb, un outils de visualisation qui s'appelle `cutter`.

on lance le binaire avec cutter, et on double clique sur main directement.
D'ici, on peux voir l'onglet `Strings`, qui fait exactement ce que la commande `strings` fait.

l'onglet `Disassembly` fait ce que gdb faisait si bien, mais le plus important, c'est l'onglet `Decompiler`.

En gros, cutter recreer le code qui une fois compile, donne le binaire.
c'est assez imbuvable, mais on peux s'y retrouver si on renomme les variables de facons humaine.

on apercois une chaine `******` dans l'onglet `Strings`, comme 'delabere', elle est suspecte.
ensuite, on vois dans le `Decompiler`, qu'il y a plein d'appel a '__syscall_malloc()'.

Petite nuance, on vois dans la liste des fonctions qu'il existe `__syscall_malloc()`, qui est une fonction `no()` deguisee.
Mais il existe aussi `____syscall_malloc()` (avec des _ en plus), qui elle remplace `yes()`.

Meme principe que l'exo2, pour proc `____syscall_malloc()` (= yes()), on doit trouver le mot de passe qui declenche strcmp().

On vois que le string comparer dans strcmp() est `*******`, on vois aussi qu'ils utilisent atoi(), comme l'exo precedent.
Et comme l'exo precedent, on vois qu'ils verifient si deux character sont bien place au debut du mot de passe, ici: `4` et `2`.

Pour le coup rien de compliquer, on fait exactement le meme processus que pour l'exo precedent; `42` au debut parce que c'est demande, puis des 7 groupe de 3 pour atoi, qui se traduisent en `*` (042).
on obtien donc `42 042 042 042 042 042 042 042` (sans les espace)







