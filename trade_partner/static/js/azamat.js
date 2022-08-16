window.addEventListener('DOMContentLoaded', () => {
    const btnAddForm = document.querySelector('#add-form')

    btnAddForm.addEventListener('click', () => {
        const productForms = document.querySelectorAll('.product-detail-form')

        productForms.forEach((productForm) => {
            const selects = document.querySelectorAll('.select2-container--default')

            selects.forEach((select, i) => {
                if(select.style.width.replace(/[^0-9\.]+/g, '') > '1' && i >= 2) {
                  select.remove()
                }
            })
            }
        )
    })
})





