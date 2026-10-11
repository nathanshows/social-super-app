# Reel: orçamento de 5 horas para 20 minutos

- **conta:** {{definir}}
- **formato:** reel, ~24 s a 180 palavras/min
- **status:** rascunho
- **gancho:** fórmula #3 Nobody Tells You, 87,0 STRONG na `hookscore_pt.py`
- **finalista alternativo:** #7 Wrong Way, Right Way, 81,4 STRONG: "Você tá fazendo orçamento errado se ainda leva cinco horas."

## Roteiro (fala)

```
Ninguém te conta: orçamento não leva 5 horas.
O meu levava. 5 horas cada um.
Eu montava tudo do zero, toda vez.
Até perceber que quase tudo se repete.
Aí montei um modelo pronto com {{o que já vem pronto}}.
Agora eu só troco {{o que muda de um cliente pro outro}}.
20 minutos. É o que leva hoje.
Comenta MODELO que eu te mando o meu.
5 horas viraram 20 minutos.
```

## Texto de tela

| tempo | card |
|---|---|
| 0:00 | ORÇAMENTO: 5 HORAS? |
| 0:02.7 | 5 HORAS CADA UM |
| 0:05.0 | TUDO DO ZERO |
| 0:07.3 | QUASE TUDO SE REPETE |
| 0:09.7 | MODELO PRONTO |
| 0:13.3 | SÓ TROCO {{o que muda}} |
| 0:17.3 | 5 H → 20 MIN |
| 0:19.7 | COMENTA "MODELO" |

## Pendências antes de gravar

- Preencher os dois `{{ }}` com o que tem de verdade no modelo.
- Ter o modelo pronto para mandar a quem comentar MODELO.

## Legenda

Termos de busca (sugestão, confirmar): "modelo de orçamento", "como fazer orçamento". Linter `caption_pt.py`: READY. `detect.py`: 68,2 REVIEW (falta especificidade: entra quando os {{ }} do modelo forem preenchidos).

```
Comenta MODELO que eu te mando o modelo de orçamento que eu uso hoje.

Cada orçamento me levava 5 horas. Hoje, 20 minutos.

Eu montava tudo do zero. Toda santa vez. Quando percebi que quase tudo se repete de um orçamento pro outro, montei um modelo pronto, e agora eu só troco o que muda de um cliente pro outro.

Se você ainda tá aprendendo como fazer orçamento, começa pelo modelo, não pela folha em branco.

#orçamento #modelodeorçamento
```
