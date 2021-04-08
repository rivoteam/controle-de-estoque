let app = new Vue({
    el: "#vue-app",
    delimiters: ['[[', ']]'],
    data() {
        return {
            produto_ean: '',
            quantidade: 1,
            produtos: [],
            valor_total: 0.00,
            errors: []
        }
    },
    computed: {
        eanIsValid() {
            this.errors = []
            return this.produto_ean.length >= 13
        }
    },
    methods: {
        validateProdutoinProdutosCart(produto_ean, quantidade) {
            console.log(produto_ean)
            var i;
            for (i = 0; i < this.produtos.length; i++) {
                console.log(this.produtos[i].produto.ean)
                if (this.produtos[i].produto.ean === produto_ean) {
                    this.produtos[i].quantidade += Number(quantidade)
                    this.errors.push("Produto já consta na lista de compra, quantidade adicionada ao produto")
                    return true
                }
            }
        },
        add_produto() {
            if (this.eanIsValid) {
                axios.get(`api-rest/produto/${this.produto_ean}`)
                    .then(response => {
                        if (response.status === 200) {
                            this.errors = []
                            if (!this.validateProdutoinProdutosCart(this.produto_ean, this.quantidade)) {
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
            axios.post("{% url 'post_realiza_vendas' %}", data = this.produtos, headers = {
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