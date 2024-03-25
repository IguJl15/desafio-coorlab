# Resultado - Desáfio CoorLab

#### Autor: Igor Julliano A. Sotero

> Estou escrevendo este documento próximo das 21:00 do dia 24/03, isto é, com um pouco de pressa, mas espero que ele esteja com os detalhes necessários para o bom entendimento do projeto e as decisões tomadas.

O desenvolvimento deste teste técnico foi bem empolgante e divertido. Um ótima experiência no geral.

## Backend

Para implementar o backend end e utilizei do framework Django que nos da diversas possibilidades e inclusive é bem mais que o necessário para este projeto. Escolhi-o por alguns motivos, mas principalmente pela velocidade na prototipação e a experiência prévia que tenho usando a ferramenta (possuo alguns meses de experiência profissional). Assim, eu poderia focar no frontend e focar em entregar uma boa experiência na princicipal interface de uso da aplicação.

Para facilitar a comunicação com o frontend, eu acoplei ao o Django Rest Framework que nos traz algumas ferramentas especificas para criação de **APIs REST** como *Serializers* e *Views* que automaticamente mapeiam suas entidades em endpoints completos

### Dos modelos relevantes

Durante o rápido desenvolvimento do backend, eu inicialmente defini a estrutura de dados dos Voos e defini seus endpoints a partir disso.

```python
class Flight(models.Model):
    company_name            = models.CharField("Company Name")
    duration                = models.DurationField("Duration")

    city_from               = models.CharField("From City")
    city_destination        = models.CharField("To City")

    price_comfort           = models.DecimalField("Price Comfort")
    price_economic          = models.DecimalField("Price Economic")
    comfort_bed_location    = models.CharField("Comfort Bed Location")
    economic_seat_location  = models.CharField("Economic Seat Location")

```
> Model simplificado para *propósito educacional*

**E isso é tudo**

Desde de que o problema do teste se baseia em adquirir informações de voos, filtra-las, e retornar, nós só precisamos desta única entidade

> **Pontos de melhoria**: Aqui acredito que poderia ser melhorado a estrutura de dados do voo normalizando a empresa e cidade (de origem e destino).  
> Em aplicações que solucionam problemas nesta área (passagens aéreas), "Voos" provavelmente seria o centro de negócios do negócio.  
> Neste exato momento existem milhares de aviões no ar e cada um está relacionado a um possível "Voo", ou seja, nós podemos e talvez deveríamos pensar em como diminuir a carga de dados deste modelo ou outras soluções para diversos problemas  
>... mas, por ora, focando em manter as coisas simples, mantemos assim.

### Filtros e organização dos dados

Definido o esquema de dados, resolvi criar o endpoint de voos que retornaria, baseado nos parâmetros, os dois itens necessários: **voo confortável e voo barato**

Pensando nisso podemos pensar no seguinte processo:


0. `Parâmetros: cidade_destino e data`
1. Buscar voos
2. Filtrar voos mantendo aqueles com `city_destination` igual ao parâmetro recebido
3. Definir **voo_barato** como, Dentre os voos encontrados, buscar aquele com o menor valor `price_economic`
3. Definir **voo_rápido** como, Dentre os voos encontrados, buscar aquele com o menor tempo de duração `duration`
3. Retornar: `{ economic: voo_barato, comfort: voo_rápido }`

> Note que a data não é utilizada. Não foi apresentado quaisquer requisitos que usam a data. O parâmetro não é validado, porém ela ainda é obrigatório
<!-- TODO: Desenvolver mais sobre isso -->

Posteriormente, eu decidi elaborar o requisito do teste para atender à seguinte proposta:

Ao informar uma cidade de destino e uma data, o usuário receberá todos os voos com o menor tempo de duração `duration`, todos os voos mais baratos com o mesmo valor `price_economic`, **e** receberá os outros voos que não se encaixam nestes filtros como sugestões para o usuário.
Essa ideia foi motivada por um recente estudo que fiz onde me deparei com algumas colocações sobre esta prática. Dizia algo como "dados de gigantes de vendas afirmam que dar sugestões de produtos relacionados àquele pesquisa pode aumentar a credibilidade com o usuário e vender X% mais"

> Alguns detalhes sobre isso: [Produtos relacionados: como usar a estratégia para aumentar as vendas no E-commerce](https://www.bis2bis.com.br/blog/produtos-relacionados/)

Com isso, surge assim a versão final do algoritmo de filtragem:

```python
todos_os_voos = Flights.objects.all(city_destination=params["city"])

minimos = todos_os_voos.aggregate(
    preco=Min("price_economic"), duracao=Min("duration")
)

voos_rapidos = todos_os_voos.filter(duration=minimos["duracao"])
voos_baratos = todos_os_voos.filter(price_economic=minimos["preco"])

todos_os_voos_encontrados = voos_baratos.union(voos_rapidos)

others = todos_os_voos.exclude(todos_os_voos_encontrados)

return Response(
    {
        "comfort": voos_rapidos,
        "economic": voos_baratos,
        "others": others,
    }
)
```
> Pseudo-código próximo ao real implementado. [Clique aqui para acessar o arquivo original](app/backend/flights/views.py)

### Adicionando voos

Para adicionar os voos disponíveis no arquivo `data.json` eu decidi criar um comando que faria o papel de ler o arquivo JSON e, para cada registro de voo, criar uma instância e salvar.

```
data = json.load(file)
flights: list[dict] = data["transport"]

for flight_json in flights:
    flight_model = Flight(
        id=flight_json["id"],
        company_name=flight_json["name"],
        city_destination=flight_json["city"],
        comfort_bed_location=flight_json["bed"],
        economic_seat_location=flight_json["seat"],
        duration=flight_json["duration"],
        price_comfort=flight_json["price_confort"],
        price_economic=flight_json["price_econ"],
        city_from="Teresina",
    )

    flight_model.save()
```
> Como o arquivo não traz consigo dados da cidade de origem, eu decidi por escrever um dado constante "Teresina" (minha cidade 🙂)
>
> ---
> Pseudo-código próximo ao real implementado. [Clique aqui para acessar o arquivo original](app/backend/flights/management/commands/loadjsondata.py)

O comando pode ser executado a partir do terminal da seguinte maneira

```bash
python3 manage.py loaddatajson ./caminho/para/data.json
```

### Autenticação e autorização

Para autenticar requests direcionadas a API REST do django, optei por usar a biblioteca Simple JWT que provê um backend de autenticação com tokens JWT para aplicações usando Django REST Framework

Sua implementação é bem rápida e fácil, o que é ótimo ja que esta funcionalidade não era necessariamente esperada no teste.

Com algumas configurações, podemos acessar os seguintes endpoints para recebermos um par de tokens JWT e realizar a operação de refresh, respectivamente

```plain
/api/tokens/
/api/tokens/refresh/
```

<!-- TODO: Desenvolver um pouco mais sobre autenticação (?) -->

## Frontend

A trajetória até o momento, utilizando Django e seus facilitadores, se fizeram necessário nesta seção pois, até o dado momento, eu não tinha tido contado com a tecnologia Vue.JS, fazendo com que eu preferisse usar uma tecnologia mais rápida para o desenvolvimento do backend, me permitindo assim, focar com calma no descobrimento desta tecnologia.

E Vue se provou magnifico. A [documentação oficial](https://vuejs.org/guide/introduction.html) ajudou bastante e foi uma das abas que ficaram abertas por mais tempo em meu navegador durante toda a semana e foi o que me guiou durante as tomadas de decisões.

Por falar em decisões

### Estrutura principal

Nas primeiras horas do desenvolvimento procurei entender qual a *filosofia*, o jeitinho fazer as coisas, do Vue.
Algumas decisões da equipe parecem muito boas, como um foco em modelo declarativo ao estruturar seus dados e a responsabilidade de entregar um modo eficiente de reatividade e gerenciamento de estados.

Com um bom entendimento e experiência prévia com outras tecnologias frontend, entender os principais conceitos e o modo de construir telas com Vue é uma tarefa fácil. 

Decidi organizar cada página (login e home) de maneira separada, separando também cada um de seus componentes. Além disso, mantive uma pequena estrutura para componentes que podem ser compartilhados entre quaisquer telas

```plain
frontend/src/views
├── components              # Componentes compartilhados
│   ├── AntDesignTheme.vue
│   └── ErrorContainer.vue
├── Auth                    # Autenticação: estado global e tela de login
│   ├── AuthState.ts
│   └── Login.vue
└── Home                    # Home: Tela Principal e seus componentes
    ├── Home.vue
    └── components
        ├── FlightItem.vue
        ├── FlightsList.vue
        └── SearchFlightsForm.vue
```

Nas telas, eu utilizei principalmente a função `ref()` para criar estados. Por exemplo, na tela inicial, temos um objeto como estado que compõe alguns itens necessários para provê uma boa experiência:

```typescript

type HomeStateData = {
  isLoading: boolean
  error: AppError | null
  data: FlightsData | null
}

const homeState = ref<HomeStateData>({
  isLoading: false,
  error: null,
  data: null
})
```
> Pseudo-código próximo ao real implementado. [Clique aqui para acessar o arquivo original](app/frontend/src/views/Home/Home.vue)

O estado é atualizado sob demanda de acordo com as ações que o usuário realiza e, para cada mudança de qualquer item desse estado, os devidos componentes dependentes do mesmo são atualizados

```typescript
async function search(formData): Promise<void> {
  try {
    // ....
  } catch (error: AppError) {
    homeState.value.error = error
  }
}

//...

// Este componente é "re-renderizado" somente
// quando o valor de `homeState.error` mudar
<ErrorContainer
  v-if="homeState.error != null"
  :error="homeState.error"
/>
```
> Código adaptado. [Clique aqui para acessar o arquivo original](app/frontend/src/views/Home/Home.vue)

#### Acessando dados da API

Para buscar os dados externos ao frontend, na API, decidi separar entidades especializadas para manter a responsabilidade fora dos códigos `.vue`, mantendo uma melhor organização

Criei dois principais Serviços para ambas funções de autenticação e "Voos"

```
frontend/src/data
├── AuthService.ts
└── FlightService.ts
```

Assim o componente Vue responsável deve utilizar das funções destes services para acessar dados


### Design

No projeto utilizei CSS 3 para diversos itens de layout. Aproveitei-me de um simples código de CSS posto na inicialização do projeto e alterei alguns detalhes que achei necessário. 

Além disso, é importante citar a utilização da biblioteca de componentes [Ant Design Vue](https://github.com/vueComponent/ant-design-vue). A biblioteca traz uma gama de componentes prontos, porém estou a usando por saber do seu poder com componentes de formulário e facilitar a validação destes mesmo formulários. Além disso, usei-a para os botões primários na aplicação.

Procurei manter um design conciso com o protótipo apresentado, porém decidi elaborar um layout diferente me inspirando principalmente no site da [Decolar.com](https://www.decolar.com/) que traz, no topo da sua tela inicial, um formulário em linha. Achei bem adequado e gostei do resultado final.

### Responsividade

Mesmo se tratando de apenas duas telas, manter um design responsivo é sempre um desafio. Decidi que em uma visualização mobile alguns elementos não seriam exibidos (nada que prejudica a usabilidade)

### Roteamento

Optei por não utilizar **Vue Router** neste projeto. Seguindo a [documentação oficial do Vue](https://vuejs.org/guide/scaling-up/routing.html), implementei um simples sistema de rotas baseado no hash da URL do site. Assim, a tela a ser exibida independe do caminho da URL (`host.com/path/feature/etc`) e responde apenas a mudanças de um último detalhe `#`. Achei interessante o uso da hash para navegação proposta pela documentação do Vue.

```typescript
const routes = {
  '/': Home,
  '/login': Login
}

const currentPath = ref(window.location.hash)

window.addEventListener('hashchange', () => {
  currentPath.value = window.location.hash
})

const currentView = computed(() => {
  const route = currentPath.value.slice(1) || '/'
  return routes[route] || NotFound
})
```
> [Arquivo original](app/frontend/src/App.vue)

Simples, funcional e, principalmente, desenvolvido de maneira ágil

## Ciclo de desenvolvimento

Desenvolvendo o teste técnico, decidi que desde o início iria manter um histórico de commits com o uso da ferramenta Git e assim foi feito. No momento que escrevo este documento o projeto conta com 35 commits realizados.

Mesmo com experiência com git flow, optei por manter todos os commits na branch principal `main` por conta das alterações se intercalarem entre dois projetos (back e front)

## Detalhes extras

### Inicialização das aplicações

Desenvolvi o script de build e inicialização ([`run.sh`](app/run.sh)) do projeto de maneira simples, mas ainda esperando algum tipo de "manutenção".

O script inicializa os processos das aplicações em **plano de fundo** e seus respectivos logs são listados em

* backend: [app/backend/logs/backend.log](app/backend/logs/backend.log)
* frontend: [app/frontend/logs/frontend.log](app/frontend/logs/frontend.log)

### Login

Para usar a aplicação, é possível realizar login com as seguintes credenciais:

username: CBAdmin
senha: admin

> As mesmas credenciais podem ser usadas para acessar o painel de administrador da aplicação backend em [`http://localhost:3000/admin`](http://localhost:3000/admin)


## O que poderia ser melhorado?

- Eu acho que o backend há muito o que melhorar e eu poderia ter dedicado-me um pouco mais em demonstrar minhas habilidades com Python
- Alguns pequenos erros podem ocorrer por conta do sistema de tokens jwt
- Alguns voos são listados em ambas categorias **conforto/rápido** e **barato**.   
    Na minha opinião, poderia ser criado uma funcionalidade exclusiva para este caso, pois ele representa um Voo que tem o valor da "classe comfort" tão barato quanto o assento "normal". Imaginei algo como "PROMOÇÃO" ou "DESTAQUE"
- Tela de login muito simples.
- Poucos elementos visuais como imagens ou textos de apresentação
- Alguns detalhes técnicos