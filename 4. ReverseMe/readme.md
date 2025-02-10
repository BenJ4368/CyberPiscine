# CyberPiscine #4: Reverse Engineering

We're in deeeeeep shit.

## Reverse me i'm famous !
>> Desassembler des binaires pour comprendre leurs fonctionnement.

### level1
On va utilise GDB, le debugger de gcc.
On lance GDB avec le binaire: `gdb binary/level1`
On liste les fonctions utilisees par le binaire: `info functions`
On desassemble la fonction main pour avoir un appercu global: `disassemble main`
Pour rendre ca plus 'lisible'(ptdr), on change la syntax assembly: `set disassembly-flavor intel` (puis re `disassemble main` pour voir la difference).

```
   Dump of assembler code for function main:
   0x565561c0 <+0>:	push   ebp
   0x565561c1 <+1>:	mov    ebp,esp
   0x565561c3 <+3>:	push   ebx
   0x565561c4 <+4>:	sub    esp,0x84
   0x565561ca <+10>:	call   0x565561cf <main+15>
   0x565561cf <+15>:	pop    ebx
   0x565561d0 <+16>:	add    ebx,0x2e31
   0x565561d6 <+22>:	mov    DWORD PTR [ebp-0x80],ebx
   0x565561d9 <+25>:	mov    DWORD PTR [ebp-0x8],0x0
   0x565561e0 <+32>:	mov    eax,DWORD PTR [ebx-0x1ff8]
   0x565561e6 <+38>:	mov    DWORD PTR [ebp-0x7a],eax
   0x565561e9 <+41>:	mov    eax,DWORD PTR [ebx-0x1ff4]
   0x565561ef <+47>:	mov    DWORD PTR [ebp-0x76],eax
   0x565561f2 <+50>:	mov    eax,DWORD PTR [ebx-0x1ff0]
   0x565561f8 <+56>:	mov    DWORD PTR [ebp-0x72],eax
   0x565561fb <+59>:	mov    ax,WORD PTR [ebx-0x1fec]
   0x56556202 <+66>:	mov    WORD PTR [ebp-0x6e],ax
   0x56556206 <+70>:	lea    eax,[ebx-0x1fea]
   0x5655620c <+76>:	mov    DWORD PTR [esp],eax
   0x5655620f <+79>:	call   0x56556060 <printf@plt>          // printf
   0x56556214 <+84>:	mov    ebx,DWORD PTR [ebp-0x80]
   0x56556217 <+87>:	lea    eax,[ebp-0x6c]
   0x5655621a <+90>:	lea    ecx,[ebx-0x1fd7]
   0x56556220 <+96>:	mov    DWORD PTR [esp],ecx
   0x56556223 <+99>:	mov    DWORD PTR [esp+0x4],eax
   0x56556227 <+103>:	call   0x56556070 <__isoc99_scanf@plt>  // scanf
   0x5655622c <+108>:	mov    ebx,DWORD PTR [ebp-0x80]
   0x5655622f <+111>:	lea    ecx,[ebp-0x6c]
   0x56556232 <+114>:	lea    edx,[ebp-0x7a]
   0x56556235 <+117>:	mov    eax,esp
   0x56556237 <+119>:	mov    DWORD PTR [eax+0x4],edx
   0x5655623a <+122>:	mov    DWORD PTR [eax],ecx
   0x5655623c <+124>:	call   0x56556040 <strcmp@plt>          // strcmp
   0x56556241 <+129>:	cmp    eax,0x0
   0x56556244 <+132>:	jne    0x56556260 <main+160>
   0x5655624a <+138>:	mov    ebx,DWORD PTR [ebp-0x80]
   0x5655624d <+141>:	lea    eax,[ebx-0x1fd4]
   0x56556253 <+147>:	mov    DWORD PTR [esp],eax
   0x56556256 <+150>:	call   0x56556060 <printf@plt>          // printf
   0x5655625b <+155>:	jmp    0x56556271 <main+177>
   0x56556260 <+160>:	mov    ebx,DWORD PTR [ebp-0x80]
   0x56556263 <+163>:	lea    eax,[ebx-0x1fc9]
   0x56556269 <+169>:	mov    DWORD PTR [esp],eax
   0x5655626c <+172>:	call   0x56556060 <printf@plt>
   0x56556271 <+177>:	xor    eax,eax
   0x56556273 <+179>:	add    esp,0x84
   0x56556279 <+185>:	pop    ebx
   0x5655627a <+186>:	pop    ebp
   0x5655627b <+187>:	ret
```

#### Essayons de faire simple avec un exemple:
`0x56556227 <+103>:	call   0x56556070 <__isoc99_scanf@plt>`
- `0x56556227`: addresse memoire de l'instruction
- `<+103>`: offset en octet depuis le debut de la fonction (ici, on est 103 octets apres le debut de main)
- `call`: nom de l'instruction (ici un appel a une fonction)
- `0x56556070`: adresse memoire de la fonction appelee
- `<__isoc99_scanf@plt>`: nom de la fonction appelee. Ici, scanf().

Si on regarde les `call`, on sait que main appel `strcmp`. Le binaire compare l'entree utilisateur de `scanf` avec une valeur, et c'est cette clef qu'on cherche.<br>Ducoup, on place un "breakpoint" sur `strcmp` avec la commande `b strcmp`. A l'execution du binaire, gdb s'arretera juste avant que le CPU n'entre dans `strcmp`, mais a cette etape les arguments de `strcmp` on deja ete places dans les registres.<br><br>
On lance l'execution du binaire avec `run` (puis des `next` si besoin), jusqu'a s'arreter sur le breakpoint (On entre une valeur reconnaissable quand le binaire nous prompt d'entree la clef). Puis, on verifie les donnees dans les registres avec `info registers` pour les afficher. On obtient dans la premiere colonne le nom de chaque registre.Google me dit que generalement, `ecx` et `edx` stock les deux arguments de `strcmp`. On print les deux avec la commande `x` pour detailler, et `/s` pour specifier le format 'string', donc `x/s $ecx` et `x/s $edx`.<br><br>L'un des deux est la valeur qu'on a entree tout a l'heure, l'autre est la clef.<br> La clef ressemble a un bout de code (c'est peut etre juste moi mdr), mais pas besoin de chercher 1h30 pour en trouver la signification (vecu), y'en a pas. On peux tester en sortant de gdb avec `quit`, en lancant le binaire et en lui donnant la clef. Tada!

Plus qu'a refaire un simple programme qui fait la meme chose et on est bon pour le level1.

### level2