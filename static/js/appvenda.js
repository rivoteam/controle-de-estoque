let app = new Vue({
    el: "#vue-app",
    delimiters: ['[[', ']]'],
    data() {
        return {
            produto_ean: '',
            quantidade: Number(1),
            produtos: [],
            valor_total: 0.00,
            errors: [],
            cpf: false,
            vendedor: '',
            numCpf: '',
            formaPagamento: ''
        }
    },
    computed: {
        eanIsValid() {
            this.errors = []
            return this.produto_ean.length >= 13
        }
    },
    methods: {
        validateProdutoinProdutosCart(produto, quantidade) {
            var i;
            if (isNaN(quantidade)) {
                this.errors.push("Quantidade precisa ser um numero valido");
                return true
            } else if (Number(quantidade) > Number(produto.total_pecas)) {
                this.errors.push("Quantidade solicitada maior que quantidade em estoque");
                return true
            } else if (Number(quantidade) <= 0) {
                this.errors.push("Insira uma quantidade válida");
                return true
            }
            for (i = 0; i < this.produtos.length; i++) {
                if (this.produtos[i].produto.ean === produto.ean) {
                    console.log(produto)
                    if ((Number(this.produtos[i].quantidade) + Number(quantidade)) > Number(produto.total_pecas)) {
                        this.errors.push("Quantidade solicitada maior que quantidade em estoque");
                        return true
                    }
                    this.valor_total = (Number(produto.preco_venda) * Number(this.quantidade)) + Number(this.valor_total)
                    this.produtos[i].quantidade = Number(quantidade) + Number(this.produtos[i].quantidade)
                    this.errors.push("Produto já consta na lista de compra, quantidade adicionada ao produto")
                    return true
                }
            }
        },
        add_produto() {
            if (this.eanIsValid) {
                axios.get(`/api-rest/produto/${this.produto_ean}`)
                    .then(response => {
                        if (response.status === 200) {
                            this.errors = []
                            if (!this.validateProdutoinProdutosCart(response.data, this.quantidade)) {
                                this.produtos.push(
                                    {
                                        'produto': response.data,
                                        "quantidade": this.quantidade
                                    }
                                )
                                this.valor_total += (Number(response.data.preco_venda) * this.quantidade)
                            }
                            this.quantidade = 1
                            this.produto_ean = ""
                        }
                    })
                    .catch(error => {
                        if (error.response.status === 404) {
                            this.errors = []
                            this.errors.push("Produto não localizado")
                        }
                        console.log(error);
                    })
            } else {
                this.errors = []
                this.errors.push("Digite um EAN com no mínimo 13 digitos")
            }
        },
        remove_produto(produto) {
            this.valor_total -= (Number(this.produtos[this.produtos.indexOf(produto)].produto.preco_venda) *
                this.produtos[this.produtos.indexOf(produto)].quantidade)
            this.produtos.splice(this.produtos.indexOf(produto), 1)
            if (this.produtos.length === 0) {
                this.valor_total = 0
            }
        },
        realiza_venda() {
            function getCookie(name) {
                let cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    const cookies = document.cookie.split(';');
                    for (let i = 0; i < cookies.length; i++) {
                        const cookie = cookies[i].trim();
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            const csrftoken = getCookie('csrftoken');
            console.log(csrftoken)
            axios.post("/api-rest/produto/realiza_vendas/", data = {
                "produtos": this.produtos,
                "vendedor": this.vendedor,
                "numerocpf": this.numCpf,
                "forma_pgto": this.formaPagamento
            }, headers = {
                'csrftoken': csrftoken
            })
                .then(response => {
                    if (response.status === 200) {
                        console.log("realizado", response)
                        location.reload()
                    }
                })
                .catch(error => {
                    console.log(error.response);
                })
        }
    }
})