function calculation(funding_amount, first_instalment, funding_period,
                    monthly_payment, total_cost_with_surcharge, bank_surcharge, credit_product){

    const selected = credit_product.options[credit_product.selectedIndex]
    const percent = selected.getAttribute('data-percent');

    const per_month_percent = parseFloat(percent.replace(",", ".")) / 12

    const bank_surcharge_value = (
        (funding_amount.value - first_instalment.value) * parseFloat(percent.replace(",", "."))
    ).toFixed(2);

    const total_cost_with_surcharge_value = parseFloat(
        bank_surcharge_value + (funding_amount.value - first_instalment.value)
    ).toFixed(2);

    if (funding_period.value != '') {
            const monthly_payment_value = (
                ((funding_amount.value - first_instalment.value) * (per_month_percent + (per_month_percent / ((1 + per_month_percent) ** funding_period.value - 1))))
            ).toFixed(2);
            monthly_payment.value = monthly_payment_value;
        }

    total_cost_with_surcharge.value = ((((funding_amount.value - first_instalment.value) * (per_month_percent + (per_month_percent / ((1 + per_month_percent) ** funding_period.value - 1))))) * funding_period.value).toFixed(2);
    bank_surcharge.value = (total_cost_with_surcharge.value - (funding_amount.value - first_instalment.value)).toFixed(2);
}

function main(){
    const funding_amount = document.getElementById('id_funding_amount');
    const funding_period = document.getElementById('id_funding_period');
    const bank_surcharge = document.getElementById('id_bank_surcharge');
    const first_instalment = document.getElementById('id_first_instalment');
    const total_cost_with_surcharge = document.getElementById('id_total_cost_with_surcharge');
    const monthly_payment = document.getElementById('id_monthly_payment');
    const credit_product = document.getElementById('id_loan_product');

    credit_product.addEventListener('change', (e) => {
        calculation(funding_amount, first_instalment, funding_period,
                    monthly_payment, total_cost_with_surcharge, bank_surcharge, credit_product
        );
    })

    first_instalment.addEventListener('change', (e) => {
        calculation(funding_amount, first_instalment, funding_period,
                    monthly_payment, total_cost_with_surcharge, bank_surcharge, credit_product
        );
    })

    funding_amount.addEventListener('change', (e) => {
        calculation(funding_amount, first_instalment, funding_period,
                    monthly_payment, total_cost_with_surcharge, bank_surcharge, credit_product
        );
    })

    funding_period.addEventListener('change', (e) => {
        calculation(funding_amount, first_instalment, funding_period,
                    monthly_payment, total_cost_with_surcharge, bank_surcharge, credit_product
        );
    })

    credit_product.addEventListener('change', (e) => {
        calculation(funding_amount, first_instalment, funding_period,
                    monthly_payment, total_cost_with_surcharge, bank_surcharge, credit_product
        );
    })

}

main()
