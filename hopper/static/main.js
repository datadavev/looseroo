
const target_input_id = "target"
const output_target_id = "output";


function setSpinner(spinner_state){
    // true to set spinner on
    // false to turn spinner off
    const ele = document.getElementById(output_target_id);
    if (spinner_state) {
        ele.innerText = "Loading...";
    } else {
        ele.innerText = "";
    }
}


async function loadUrl(url) {
    setSpinner(true);
    var api_url = "/" + encodeURIComponent(url);
    try {
        const response = await fetch(api_url);
        const data = await response.json();
        const ele = document.getElementById(output_target_id);
        setSpinner(false)
        ele.innerText = JSON.stringify(data, null, 2);
    } catch (error) {
        setSpinner(false)
        const ele = document.getElementById(output_target_id);
        ele.innerText = error;
    }
}

function doLoadUrl() {
    const target_ele = document.getElementById(target_input_id);
    const url = target_ele.value;
    loadUrl(url);
}
