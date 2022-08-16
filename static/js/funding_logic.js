const btn = document.querySelector('#id_loan_product')
const fundingAmount = document.querySelector('#id_funding_amount')
const firstInstalment = document.querySelector('#id_first_instalment')
const hintFirstInstalment = document.querySelector('#hint_id_first_instalment')


btn.addEventListener('click', () => {

    const payment_values = []

    loan_initial_payment_values.forEach(loan_initial_payment_value => {
        payment_values.push(parseInt(loan_initial_payment_value['fields']['total_cost'], 10))
    })

    const productPrices = document.querySelectorAll('.product-price')
    let totalProductPrices = 0
    productPrices.forEach(productPrice => {
            if (productPrice.value){
                totalProductPrices += parseInt(productPrice.value, 10)
            }
    })
    payment_values.push(totalProductPrices)
    console.log(totalProductPrices)

    payment_values.sort(function(a, b) {
            return a - b;
        })

    payment_value_index = payment_values.indexOf(totalProductPrices)
    console.log(payment_value_index, payment_values, payment_values.length)

    if (payment_value_index != 0) {

        loan_initial_payment_values.forEach(loan_initial_payment_value => {
            if (payment_values[payment_value_index-1] == parseInt(loan_initial_payment_value['fields']['total_cost'], 10)){
                minFirstInstalment = (totalProductPrices * loan_initial_payment_value['fields']['initial_payment_percent']).toFixed(2)
                firstInstalment.setAttribute('min', minFirstInstalment)
                firstInstalment.value = minFirstInstalment
                hintFirstInstalment.innerHTML = `сом (мин-${minFirstInstalment})`
            }

        })
    }
    fundingAmount.value = totalProductPrices
})

