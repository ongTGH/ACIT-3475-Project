/* Overview percentage bar on homepage
-------------------------------------------*/

categoryPercentLabel = document.querySelectorAll(".percent-label");

for(let category of categoryPercentLabel) {
  percentage = category.querySelector("label").textContent.replace(" Spent", "");
  if (category.querySelector(".percentage")) {
    percentageGauge = category.querySelector(".percentage");
    percentageGauge.style.width = percentage;
  }
}


/* side bar menu
-------------------------------------------*/

closeButton = document.querySelector("#side-menu-close")
sideMenu = document.querySelector("#menu-expand")
menuIcon = document.querySelector(".menu-btn")

function openMenu() {
    sideMenu.style.width = "200px";
    sideMenu.classList.toggle("menu-display");
}

menuIcon.addEventListener("click", openMenu)

function closeMenu() {
    if (sideMenu.style.width !== "0") {
        sideMenu.style.width = "0";
    }
}

closeButton.addEventListener("click", closeMenu)


/* alert message */

const alertPlaceholder = document.getElementById('liveAlertPlaceholder')
const appendAlert = (message, type) => {
  const wrapper = document.createElement('div')
  wrapper.innerHTML = 
    `<div class="alert alert-primary d-flex align-items-center" role="alert" data-bs-dismiss="alert" id="alert-box">
  <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-exclamation-circle" viewBox="0 0 16 16">
    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
    <path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/>
  </svg>
  <div>
    Cannot make this transaction
  </div>
</div>`

  alertPlaceholder.append(wrapper)

  setTimeout(() => {
  
    // removes element from DOM
    wrapper.style.display = "none"
  
    // hides element (still takes up space on page)
    // box.style.visibility = 'hidden';
  }, 3000); // time in milliseconds
}


const alertTrigger = document.getElementById('liveAlertBtn')
if (alertTrigger) {
  alertTrigger.addEventListener('click', () => {
    appendAlert("", 'success')
  })
}



/* categories page 
-------------------------------------------*/

const categoriesList = document.querySelectorAll(".category")
const budgetDropDown = document.querySelectorAll(".budget-dropdown")

let categoryIndex = 0;
let compareIndex = 0;

for(let category of categoriesList){
    category.addEventListener("click", (e) => {
        let categoryName = ""
        console.log(e.target)
        if (e.target.classList.contains("category")) {
            categoryName = e.target.querySelector("h4").textContent
        }

        else if (e.target.classList.contains("category-budget")){
            categoryName = e.target.parentElement.querySelector("h4").textContent
            console.log(categoryName)
        }

        else {
            categoryName = e.target.parentElement.parentElement.querySelector("h4").textContent
        }

        category.classList.toggle("category-clicked");
        if (category.classList.contains("category-clicked")){

            for(let budget of budgetDropDown) {

                const original_id = budget.id

                if (categoryName === budget.id){

                  if (budget.id.includes(" ")) {
                    budget.id = budget.id.trim().replaceAll(" ", "-")
                  }
              
                  if(budget.id.includes("'")) {
                    budget.id = budget.id.replaceAll("'", "")
                  }

                    dropDownItems = document.querySelector("#" + budget.id).querySelectorAll(".budget-item")
                    dropDownHeight = 100 * dropDownItems.length
                    document.querySelector("#" + budget.id).style.height = `${dropDownHeight}px`;

                  budget.id = categoryName
                }
            }
        }

        else {
        for(let budget of budgetDropDown) {

            if (categoryName === budget.id){

              if (budget.id.includes(" ")) {
                budget.id = budget.id.trim().replaceAll(" ", "-")
              }
          
              if(budget.id.includes("'")) {
                budget.id = budget.id.replaceAll("'", "")
              }

                document.querySelector("#" + budget.id).style.height = "0";

              budget.id = categoryName

            }
        }
        }
    });
}

editCategories = document.getElementById("edit-categories")
categoryButtons = document.querySelectorAll(".cat-btns-div")

function categoryEditMode() {
  for(let button of categoryButtons){
    console.log(button.style.overflow)
    if (button.style.overflow === "visible"){
      button.style.overflow = "hidden"
      button.style.height = "0"
      button.querySelector(".btn-secondary").style.height = "0"
      button.querySelector(".btn-danger").style.height = "0"
      editCategories.querySelector("button").textContent = "Edit Categories"

    }
    else{
      button.style.overflow = "visible"
      button.style.height = "50px"
      button.querySelector(".btn-secondary").style.height = "50px"
      button.querySelector(".btn-danger").style.height = "50px"
      editCategories.querySelector("button").textContent = "Quit Edit Mode"
    }

  }


}

// editCategories.addEventListener("click", categoryEditMode)


// category page popup menus

const editButton = document.querySelectorAll(".edit-btn")

for (let button of editButton){
  button.addEventListener("click", (e)=> {
    if (e.target.id.includes(" ")) {
      e.target.id = e.target.id.trim()
    }

    if(e.target.id.includes("'")) {
      e.target.id = e.target.id.replaceAll("'", "")
    }

    let idName = e.target.id
    let categoryNameToEdit = idName.replace("edit-", "").trim()

    console.log(categoryNameToEdit)

    if (categoryNameToEdit.includes(" ")) {
      categoryNameToEdit = categoryNameToEdit.trim().replaceAll(" ", "-")
    }

    if(categoryNameToEdit.includes("'")) {
      categoryNameToEdit = categoryNameToEdit.replaceAll("'", "")
    }

    let editPopUp = document.querySelector("#edit-popup-" + categoryNameToEdit)
    let editBackground = document.querySelector("#edit-background-" + categoryNameToEdit)
    editPopUp.classList.toggle("category-edit-clicked")
    editBackground.classList.toggle("category-edit-clicked")
  })
}

categoryEditPopup = document.querySelectorAll(".category-edit-popup")
popupBackground = document.querySelectorAll(".category-edit-background")

for (let background of popupBackground) {
  background.addEventListener("click", ()=> {
    for (let popup of categoryEditPopup) {
      if (popup.classList.contains("category-edit-clicked")) {
        popup.classList.toggle("category-edit-clicked")
        background.classList.toggle("category-edit-clicked")
      }
    }
  })
}

const deleteCategoryButton = document.querySelectorAll(".delete-category")
const deleteCategoryPopup = document.querySelectorAll(".category-delete-popup")

for (let button of deleteCategoryButton) {
  button.addEventListener("click", (e) => {
    if (e.target.id.includes(" ")) {
      e.target.id = e.target.id.trim().replace(" ", "-")
    }

    if(e.target.id.includes("'")) {
      e.target.id = e.target.id.replace("'", "")
    }

    let idName = e.target.id
    let categoryNameToDelete = idName.replace("delete-", "").trim()

    if (categoryNameToDelete.includes(" ")) {
      categoryNameToDelete = categoryNameToDelete.trim().replaceAll(" ", "-")
    }

    if(categoryNameToDelete.includes("'")) {
      categoryNameToDelete = categoryNameToDelete.replaceAll("'", "")
    }

    console.log(categoryNameToDelete)

    let deletePopUp = document.querySelector("#delete-category-" + categoryNameToDelete)
    let deleteBackground = document.querySelector("#delete-background-" + categoryNameToDelete)
    deletePopUp.classList.toggle("category-delete-clicked")
    deleteBackground.classList.toggle("category-delete-clicked")

  }) 
}

// Expense page
document.addEventListener('DOMContentLoaded', (event) => {
  let budgetNames = document.querySelectorAll(".clear-expenses-button").forEach((button) => {
      button.addEventListener('click', () => {
          let budgetName = button.id.replace('clear-expenses-', '');
          fetch(`${window.location.origin}/clear_expenses/${budgetName}`, {method: 'DELETE'})
              .then(response => response.json())
              .then(data => {
                  if (data.status === 'success') {
                      location.reload();
                  }
              })
              .catch(error => console.error('Error:', error));
      });
  });
});
