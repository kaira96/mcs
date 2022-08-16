const btnAddForm = document.querySelector('#add-form')

btnAddForm.addEventListener('click', () => {
    const productForms = document.querySelectorAll('.product-detail-form')

    productForms.forEach(productForm => {
        const selects = document.querySelectorAll('.select2-container--default')

        selects.forEach(select => {
            console.log(select)
            const selectChild = select.querySelector('.dropdown-wrapper')
            if(selectChild && select.style.width === '550px') {

              select.remove()
            }
        })
        }
    )
})



