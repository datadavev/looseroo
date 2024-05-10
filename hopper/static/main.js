const url_pattern = new RegExp(/https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)?/gi);
const target_input_id = "target"
const output_target_id = "output";
const accept_input_id = "accept";
const white_input_id = "whitehosts";


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


async function loadUrl(url, accept, whitehosts) {
    setSpinner(true);
    let api_url = new URL("/" + encodeURIComponent(url.trim()), document.location.href);
    api_url.searchParams.append("accept", accept.trim());
    if (whitehosts.length > 0) {
        api_url.searchParams.append("whitehosts", whitehosts.trim());
    }
    try {
        const response = await fetch(api_url.href);
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
    const url = document.getElementById(target_input_id).value;
    const accept = document.getElementById(accept_input_id).value;
    const whitehosts = document.getElementById(white_input_id).value;
    loadUrl(url, accept, whitehosts);
}
