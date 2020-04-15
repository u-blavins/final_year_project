var currentTab = 0; // Current tab is set to be the first tab (0)
showTab(currentTab); // Display the current tab

var configurations = {
    0: 'BucketName',
    1: 'AccelerateConfiguration',
    2: 'AccessControl',
    3: 'AnalyticsConfiguration',
    4: 'Test'
}

var payload = {}

function showTab(n) {
  // This function will display the specified tab of the form ...
  var x = document.getElementsByClassName("tab");
  x[n].style.display = "block";

  if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }
  if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }
  fixStepIndicator(n)
}

function nextPrev(n) {
  // This function will figure out which tab to display
  var x = document.getElementsByClassName("tab");
  // Exit the function if any field in the current tab is invalid:
  if (n == 1 && !validateForm()) return false;
  // Hide the current tab:
  x[currentTab].style.display = "none";
  // Increase or decrease the current tab by 1:
  currentTab = currentTab + n;
  // if you have reached the end of the form... :
  if (currentTab >= x.length) {
    //...the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
  }
  // Otherwise, display the correct tab:
  showTab(currentTab);
}

function validateForm() {
    // This function deals with validation of the form fields
    var x, config, valid = true;
    x = document.getElementsByClassName("tab");
    config = configurations[currentTab];
    if (config == "BucketName") {
        valid = validateBucketName(x, config);
    } else if (config == "AccelerateConfiguration") {
        valid = validateBucketName(x, config);
    }

    if (valid) {
        document.getElementsByClassName("step")[currentTab].className += " finish";
    }
    return valid; // return the valid status
}

function validateBucketName(x, config) {
    valid = true;
    y = x[currentTab].getElementsByTagName("input");
    if (y[0].value == "") {
        y[0].className += " invalid";
        valid = false;
    }
    return valid;
}

function fixStepIndicator(n) {
    var i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
        x[i].className = x[i].className.replace(" active", "");
    }
    x[n].className += " active";
}