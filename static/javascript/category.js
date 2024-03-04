/* categories page */

const categoriesList = document.querySelectorAll(".category")
const budgetDropDown = document.querySelectorAll(".budget-dropdown")
editCategories = document.getElementById("edit-categories").querySelector("button")

let categoryIndex = 0;
let compareIndex = 0;

for (let budget of budgetDropDown) {
    budget.style.height = "0"
    console.log(budget.style.height)
}


for(let category of categoriesList){
    category.addEventListener("click", (e) => {
        let categoryName = ""
        if (e.target.classList.contains("category")) {
            categoryName = e.target.querySelector(".left-side").querySelector("h4").textContent
        }

        else if (e.target.classList.contains("category-budget")){
            categoryName = e.target.parentElement.querySelector(".left-side").querySelector("h4").textContent
            console.log(categoryName)
        }

        else if(e.target.classList.contains("left-side")){
            categoryName = e.target.querySelector("h4").textContent
        }

        else {
            categoryName = e.target.parentElement.querySelector("h4").textContent
        }

        if (editCategories.textContent === "Edit Categories"){
            for (let budget of budgetDropDown) {
                if (categoryName === budget.id) {
                    if (budget.querySelectorAll(".budget-item")){
                    dropDownItems = budget.querySelectorAll(".budget-item")
                        if (dropDownItems.length > 0) {
                            category.classList.toggle("category-clicked");
                        }
                    }
                }
            }
        }

        if (category.classList.contains("category-clicked")) {

            for(let budget of budgetDropDown) {

                if (categoryName === budget.id && editCategories.textContent === "Edit Categories") {

                    for (otherBudget of budgetDropDown) {
                        if (otherBudget.style.height !== "0px") {
                            otherBudget.style.height = "0"
                            otherBudget.style.zIndex = "0"
                            otherBudget.parentElement.parentElement.querySelector(".category").classList.toggle("category-clicked")
                        }
                    }

                    if (budget.id.includes(" ")) {
                        budget.id = budget.id.trim().replaceAll(" ", "-")
                    }
                
                    if (budget.id.includes("'")) {
                        budget.id = budget.id.replaceAll("'", "")
                    }

                    dropDownItems = document.querySelector("#" + budget.id).querySelectorAll(".budget-item")
                    dropDownHeight = 115 * dropDownItems.length
                    document.querySelector("#" + budget.id).style.height = `${dropDownHeight}px`;
                    budget.style.zIndex = "100"
                    budget.parentElement.style.zIndex = "100"
                    // document.querySelector("#" + budget.id).style.zIndex = "10"
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
                    budget.style.zIndex = "0"
                    budget.id = categoryName
                }
            }
        }

    });
}


categoryButtons = document.querySelectorAll(".cat-btns-div")


function categoryEditMode() {
    for(let button of categoryButtons){
        console.log(button.style.overflow)
        if (button.style.overflow === "visible"){
            button.style.overflow = "hidden"
            button.style.height = "0"
            button.querySelector(".btn-secondary").style.height = "0"
            button.querySelector(".btn-danger").style.height = "0"
            editCategories.textContent = "Edit Categories"
        }
        else{
            button.style.overflow = "visible"
            button.style.height = "50px"
            button.querySelector(".btn-secondary").style.height = "50px"
            button.querySelector(".btn-danger").style.height = "50px"
            editCategories.textContent = "Quit Edit Mode"
            for(let budget of budgetDropDown) {
                if (budget.style.height !== "0") {
                    budget.style.height = "0"
                }
            }
            for(let category of categoriesList) {
                if (category.classList.contains("category-clicked")){
                    category.classList.toggle("category-clicked")
                }
            }
        }
    }
}

editCategories.addEventListener("click", categoryEditMode)



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

categoryEditExit = document.querySelectorAll(".edit-popup-exit")

for (let exitButton of categoryEditExit) {
    exitButton.addEventListener("click", ()=> {
        for (let popup of categoryEditPopup) {
            if (popup.classList.contains("category-edit-clicked")) {
                popup.classList.toggle("category-edit-clicked")
            }
        }
        for (let background of popupBackground) {
            if (background.classList.contains("category-edit-clicked")) {
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
        console.log(document.querySelector("#delete-category-Living-Expenses"))
        let deletePopUp = document.querySelector("#delete-category-" + categoryNameToDelete)
        let deleteBackground = document.querySelector("#delete-background-" + categoryNameToDelete)
        deletePopUp.classList.toggle("category-delete-clicked")
        deleteBackground.classList.toggle("category-delete-clicked")
    })
}