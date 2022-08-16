const mySelect = document.querySelector("#id_client-is_married");
const toggleBlock = document.querySelector(".spouse");

const jobBlock = document.querySelector(".client-job");
const jobCommercialBlock = document.querySelector(".client-commercial");
const jobTypeSelect = document.querySelector("#client-job-type-select");

mySelect.addEventListener("change", (e) => {
  let value = e.target.value;
  if (e.target.value === "False") {
    toggleBlock.classList.add("active-married-form");
  } else {
    toggleBlock.classList.remove("active-married-form");
  }
});

jobTypeSelect.addEventListener('change', (e) => {
    let value = e.target.value;
    console.log(123)
    if (e.target.value === "True") {
        jobBlock.classList.remove("active-job-form");
        jobCommercialBlock.classList.add("active-commercial-form");
    } else {
        jobBlock.classList.add("active-job-form");
        jobCommercialBlock.classList.remove("active-commercial-form");
    }
})

function setDataByPin(formName) {

    const pin_input = document.getElementById(`id_${formName}-pin`);
    const gender_select = document.getElementById(`id_${formName}-gender`);
    const date_of_birth_input = document.getElementById(`id_${formName}-date_of_birth`);

    pin_input.addEventListener('change', (e) => {
        const gender = e.target.value[0];
        const day_of_birth = e.target.value.slice(1, 3);
        const month_of_birth = e.target.value.slice(3, 5);
        const year_of_birth = e.target.value.slice(5, 9);

        if (gender === "2") {
            gender_select.selectedIndex = 1
        }
        else if (gender === "1") {
            gender_select.selectedIndex = 2
        }
        else {
            gender_select.selectedIndex = 0
        }

        if (e.target.value.length == 14) {
            date_of_birth_input.value = `${year_of_birth}-${month_of_birth}-${day_of_birth}`
        }
    })
}

setDataByPin("client");
setDataByPin("spouse");
setDataByPin("guarantor");