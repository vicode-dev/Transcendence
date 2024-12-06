const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

let backgroundColor = window.getComputedStyle(document.documentElement).getPropertyValue('--background-color');
let secondaryColor = window.getComputedStyle(document.documentElement).getPropertyValue('--secondary-color');
let accentColor = window.getComputedStyle(document.documentElement).getPropertyValue('--accent-color');

const originalScripts = new Set();
const scripts = document.querySelectorAll('script');
scripts.forEach(script => originalScripts.add(script));
// window.addEventListener('DOMContentLoaded', function () {
// console.log("Captured original scripts:", originalScripts);
// });


redirect();

function redirect() {
    searchUrl = new URLSearchParams(window.location.search);
    if(searchUrl.has("redirect_url"))
    {
        new_url = searchUrl.get("redirect_url")
        searchUrl.delete("redirect_url")
        if (searchUrl.size > 0)
            new_url += "?" + searchUrl.toString();
        loadPage(new_url);
    }
    else
    {
        loadPage("/home/");
    }
    // else load page /home
}

function loadPageEvent(event, url) {
    event.preventDefault();
    loadPage(url);
}

function loadPage(url) {
    console.log("Load Page", url);
    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            // redirect: 'manual'
        }
    })
        .then(response => {
            if (response.status == 302)
                return loadPage(response.headers.get('Location'));
            if (response.ok) {
                return response.text();
            }
            throw new Error('Network response was not ok');
        })
        .then(html => {
            document.getElementById('content').innerHTML = html;
            // const loadedPartial = document.querySelector('[data-partial]').getAttribute('data-partial');
            // initializeScriptsForPartial(loadedPartial);
            // unloadScripts();
            initializeScriptsForPartial(originalScripts);
            window.history.pushState({ path: url }, '', url);
            checkTournament();
        })
        .catch(error => {
            console.error('There was a problem with the fetch operation:', error);
        });
    // loadPageContent(url);
    // initializeScriptsForPartial(originalScripts);
    // window.history.pushState({ path: url }, '', url);
}

window.addEventListener('popstate', (event) => {
    // event.preventDefault();
    console.log(event.state, event.state.path);
    if (event.state && event.state.path) {
        loadPageContent(event.state.path);
    }
});

function unloadScripts() {
    document.querySelectorAll('script').forEach(script => {
        console.log('removing script: ', script);
        script.remove();
    });
}

function loadPageContent(url) {
    console.log("Load Page Content", url);
    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
        .then(response => response.text())
        .then(html => {
            document.getElementById('content').innerHTML = html;
        })
        .catch(error => {
            if(error.status == 404)
            {document.getElementById('content').innerHTML = html}
            console.error('There was a problem with the fetch operation:', error);
        });
}

const loadedScripts = new Set(); //sinon utliser local storage
function loadScriptOnce(src, callback) {

    // const scriptUrl = new URL(src, window.location.href);
    // const scriptPath = scriptUrl.pathname;
    // const scriptHref = scriptUrl.href;

    // console.log("Attempting to load script:", src);
    if (loadedScripts.has(src)) {
        // || loadedScripts.has(scriptHref)) {
        console.log('Script already loaded:', src);
        callback();
        return;
    }
    const script = document.createElement('script');
    script.src = src;
    script.type = 'text/javascript';
    script.onload = () => {
        // console.log('Script loaded successfully:', src);
        loadedScripts.add(src);
        // loadedScripts.add(scriptUrl.href);
        // window.scriptLoaded = true;
        callback();
    };
    script.onerror = () => {
        console.error(`Error loading script: ${src}`);
    };
    // document.head.appendChild(script);
    document.body.appendChild(script);

    // console.log('Script tag appended:', src);
}

function initializeScriptsForPartial(originalScripts) {
    console.log("Initialize script")
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            console.log('DOM fully loaded');
            loadAllScripts(originalScripts);
        });
    } else {
        console.log('DOM already loaded');
        loadAllScripts(originalScripts);
    }
}

function loadAllScripts(originalScripts) {
    const scripts = document.querySelectorAll('script');

    scripts.forEach(script => {
        const scriptSrc = script.src;
        if (scriptSrc && !loadedScripts.has(scriptSrc)) {

            const scriptUrl = new URL(scriptSrc);
            // const scriptPath = scriptUrl.pathname;
            for (const originalScript of originalScripts) {
                if (script.getAttribute('src') === originalScript.getAttribute('src')) {
                    // console.log("ORIGINAL MATCH: ", originalScript);
                    return;
                }
            }

            loadScriptOnce(scriptSrc, () => {
                console.log('Script loaded successfully:', scriptSrc);
                // originalScripts.add(script);
                // console.log('Script removing:', scriptSrc);
                // delete window.scriptLoaded;
                // script.remove();
            });

        } else {
            // console.log('Script not found or already loaded: ',  scriptSrc);
            // script.remove();
        }
    });
}