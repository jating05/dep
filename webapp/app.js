let cacheData = null
let selectedItems = [];


document.addEventListener('DOMContentLoaded', () => {
    const multiSelectContainer = document.querySelector('.multi-select-container');
    const selectedItemsContainer = document.getElementById('selected-items');
    const dropdown = document.getElementById('dropdown');
    const optionsList = document.getElementById('options-list');
    const searchInput = document.getElementById('search-input');

    const options = [
      'Apply',
      'Communication',
      'Lilac',
      'Digital',
      'Mobile'
    ];
   
    function renderOptions(filter = '') {
      optionsList.innerHTML = '';
      const filteredOptions = options.filter(option => 
        option.toLowerCase().includes(filter.toLowerCase()) &&
        !selectedItems.includes(option)
      );

      if (filteredOptions.length === 0) {
        const li = document.createElement('li');
        li.textContent = 'No options found';
        li.classList.add('no-options');
        optionsList.appendChild(li);
        return;
      }

      filteredOptions.forEach(option => {
        const li = document.createElement('li');
        li.textContent = option;
        li.addEventListener('click', () => selectItem(option));
        optionsList.appendChild(li);
      });
    }

  
    function renderSelectedItems() {
      // Remove all existing selected item tags except the input field
      selectedItemsContainer.querySelectorAll('.selected-item').forEach(item => item.remove());

      selectedItems.forEach(item => {
        const div = document.createElement('div');
        div.classList.add('selected-item');

        const span = document.createElement('span');
        span.textContent = item;

        const removeBtn = document.createElement('span');
        removeBtn.classList.add('remove-item');
        removeBtn.textContent = '×';
        removeBtn.setAttribute('aria-label', `Remove ${item}`);
        removeBtn.title = `Remove ${item}`;
        removeBtn.addEventListener('click', (e) => {
          e.stopPropagation(); // Prevent triggering the container's click event
          removeItem(item);
        });

        div.appendChild(span);
        div.appendChild(removeBtn);
        selectedItemsContainer.insertBefore(div, searchInput);
      });
    }


    function selectItem(item) {
      selectedItems.push(item);
      renderSelectedItems();
      renderOptions(searchInput.value);
      searchInput.value = '';
      searchInput.focus();
    }

  
    function removeItem(item) {
      selectedItems = selectedItems.filter(i => i !== item);
      renderSelectedItems();
      renderOptions(searchInput.value);
    }

 
    function toggleDropdown(show) {
      dropdown.style.display = show ? 'block' : 'none';
      if (show) {
        renderOptions(searchInput.value);
      }
    }

   
    function handleClickOutside(e) {
      if (!multiSelectContainer.contains(e.target)) {
        toggleDropdown(false);
      }
    }

  
    function handleKeyboard(e) {
      switch (e.key) {
        case 'ArrowDown':
          e.preventDefault();
          focusNextOption();
          break;
        case 'ArrowUp':
          e.preventDefault();
          focusPreviousOption();
          break;
        case 'Enter':
          e.preventDefault();
          const focused = document.activeElement;
          if (focused && focused.parentElement === optionsList) {
            focused.click();
          }
          break;
        case 'Escape':
          toggleDropdown(false);
          break;
        default:
          break;
      }
    }

    function focusNextOption() {
      const options = dropdown.querySelectorAll('li:not(.no-options)');
      if (options.length === 0) return;
      let index = Array.from(options).findIndex(option => option === document.activeElement);
      if (index < options.length - 1) {
        options[index + 1].focus();
      }
    }

   
    function focusPreviousOption() {
      const options = dropdown.querySelectorAll('li:not(.no-options)');
      if (options.length === 0) return;
      let index = Array.from(options).findIndex(option => option === document.activeElement);
      if (index > 0) {
        options[index - 1].focus();
      }
    }

    renderOptions();


    multiSelectContainer.addEventListener('click', () => {
      toggleDropdown(true);
      searchInput.focus();
    });

    document.addEventListener('click', handleClickOutside);

    // Filter options based on input
    searchInput.addEventListener('input', (e) => {
      renderOptions(e.target.value);
      toggleDropdown(true);
    });

    searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Backspace' && searchInput.value === '') {
        if (selectedItems.length > 0) {
          removeItem(selectedItems[selectedItems.length - 1]);
        }
      }
    });

    searchInput.addEventListener('keydown', handleKeyboard);

    optionsList.addEventListener('keydown', handleKeyboard);
 
    console.log(1);
  });

//Function to fetch the logs and display them on the dashboard
async function loadDashboardData() {
    try{
        const response = await fetch('http://127.0.0.1:5000/get_logs',{
            method:'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const result = await response.json();

        if(response.status == 200){
            displayLogs(result.logs);
        }else{
            alert('Error fetching data: ' + result.error);
        }

    } catch (error){
        console.error('Error fetching data:', error);
    }
}

// Function to diplay logs in dashboard
function displayLogs(logs) {
    const logsTable = document.getElementById('logsTable').getElementsByTagName('tbody')[0];
    logsTable.innerHTML = '';//clear the table

    logs.forEach(log => {
        const row = document.createElement('tr');
        if (log.conflictAttachment == "No Conflict"){
            row.innerHTML = `
            <td>${log.obn}</td>
            <td>${log.projectName}</td>
            <td>${log.goLiveDate}</td>
            <td>${log.deploymentStartDate}</td>
            <td>${log.deploymentEndDate}</td>
            <td>${log.devName}</td>
            <td>${log.qeName}</td>
            <td>${log.impactedChannels}</td>
            <td>${log.conflict ? 'Yes' : 'No'}</td>
            <td>${log.conflictAttachment}</td>
            `;
            logsTable.appendChild(row);
        } else{
            row.innerHTML = `
            <td>${log.obn}</td>
            <td>${log.projectName}</td>
            <td>${log.goLiveDate}</td>
            <td>${log.deploymentStartDate}</td>
            <td>${log.deploymentEndDate}</td>
            <td>${log.devName}</td>
            <td>${log.qeName}</td>
            <td>${log.impactedChannels}</td>
            <td>${log.conflict ? 'Yes' : 'No'}</td>
            <td><a href="${log.conflictAttachment}" />${log.conflictAttachment}</td>
            `;
            logsTable.appendChild(row);
        }
    });
}




// Function to handle form submission for log entry
const form = document.getElementById('deployment-form')
form.addEventListener('submit',async function(event) {
    event.preventDefault();
console.log("button clicked")
    const logData = {
        obn: document.getElementById('obn').value,
        projectName: document.getElementById('projectName').value,
        goLiveDate: document.getElementById('goLiveDate').value,
        deploymentStartDate: document.getElementById('deplStartDate').value,
        deploymentEndDate: document.getElementById('deplEndDate').value,
        devName: document.getElementById('devName').value,
        qeName: document.getElementById('qeName').value,
        // impactedChannels: Array.from(document.getElementById('impactedChannels').selectedOptions).map(opt => opt.value)
        impactedChannels : selectedItems
      
      };
      if(logData.deploymentStartDate>logData.deploymentEndDate){
            alert('Error : Deployment start date is later than the deployment end date');
        }
        if(logData.goLiveDate<logData.deploymentEndDate){
          alert('Error : Testing end date is later than the Go Live date');
      }
    try{
            const response = await fetch('http://127.0.0.1:5000/submit_log',{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(logData)
            });
        // }
        const result = await response.json();
        if (response.status === 200){
            loadDashboardData();
            document.getElementById('form-feedback').textContent = 'Log Submitted Successfully';
        }else{
            //check for conflict and trigger popup if necessary
            if (result.conflict) {
                cacheData = result.conflictData;
                // return result.conflictData;
                // console.log(result.conflict);
                openPopup(result);
            }
        }

    }catch(error){
        console.log(4);
        console.error('Error Submitting form:',error);
    }
});

// Function to open the conflict resolution popup
function openPopup(result) {
    document.getElementById('popup').style.display = 'flex';

    let popupContent = '<h10>Conflicts:</h10>';

    if (result.conflict && result.conflictDetails.length > 0) {
        result.conflictDetails.forEach((detail, index) => {
            popupContent += `
            <div>
                <label>
                    <input type="checkbox" class="conflict-checkbox">
                    <strong>Project Name:</strong> ${detail.projectName},
                    <strong>Developer:</strong> ${detail.developer},
                    <strong>QE:</strong> ${detail.qe}
                </label>
            </div>`;
        });
    }

    document.getElementById('popup-content').innerHTML = popupContent;

    // Get the submit button and disable it initially
    const submitButton = document.getElementById('submitAttachment');
    submitButton.disabled = true;

    // Select all checkboxes
    const checkboxes = document.querySelectorAll('.conflict-checkbox');

    // Function to check if all checkboxes are checked
    function checkCheckboxes() {
        const allChecked = Array.from(checkboxes).every(checkbox => checkbox.checked);
        submitButton.disabled = !allChecked;
    }

    // Add event listeners to checkboxes
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', checkCheckboxes);
    });
}

//Function to close the popup 
function closePopup(){
 document.getElementById('popup').style.display = 'none';
}

//Handle file attachment submission for conflict resolution
document.getElementById('submitAttachment').addEventListener('click',async function async () {

    const attachment = document.getElementById('attachment').files[0];

    if (!attachment) {
        alert('Please attach the email proof');
        return;
    }

    const formData = new FormData();
    formData.append('conflictAttachment',attachment)

    try{
        const response = await fetch('http://127.0.0.1:5000/resolve_conflict',{
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (response.status === 200){
            alert('Conflict resolved successfully.');
            loadDashboardData(); //reload logs
            closePopup(); //close popup
        }else{
            alert('Error resolving conflict: ' + result.error);
        }
    } catch (error){
        console.error('Error submitting attachment:', error);
    }
});
// function filterOptions(){
//     const input=document.getElementById("searchInput");
//     const filter = input.value.toLowerCase();
//     const ul=document.getElementById("ImpactedChannels").getElementsByTagName("ul")[0];
//     const li =ul.getElementsByTagName("li");

//     for(let i=0;i<li.length;i++){
//         const label=li[i]/getElementsByTagName("label")[0];
//         const textValue = label.textContent || label.innerText;
//         li[i].style.display = textValue.toLowerCase().indexOf(filter) > -1 ? "" :"none";
//     }
// }
// Load initial data
loadDashboardData();

