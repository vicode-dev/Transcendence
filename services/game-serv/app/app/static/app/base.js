const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

// let backgroundColor = window.getComputedStyle(document.documentElement).getPropertyValue('--background-color');
// let secondaryColor = window.getComputedStyle(document.documentElement).getPropertyValue('--secondary-color');
// let accentColor = window.getComputedStyle(document.documentElement).getPropertyValue('--accent-color');

const originalScripts = new Set();
const scripts = document.querySelectorAll('script');
scripts.forEach(script => originalScripts.add(script));

let destructors = [];
let mains = new Map();

redirect();
function redirect() {
    let searchUrl = new URLSearchParams(window.location.search);
    if(searchUrl.has("redirect_url") && !window.history.state?.fromBack)
    {
        new_url = searchUrl.get("redirect_url")
        searchUrl.delete("redirect_url")
        if (searchUrl.size > 0)
            new_url += "?" + searchUrl.toString();
            loadPage(new_url).then();
    }
    else
    {
        loadPage("/home/").then();
    }
}

function loadPageEvent(event, url) {
    event.preventDefault();
    loadPage(url).then();
}

/**
 * 
 * @param {string} url 
 * @param {boolean} update_url 
 * @returns {string}
 */
async function loadPage(url, update_url = true) {
    destructors.forEach(destructor => destructor());
    destructors = [];

    // let cleanUrl = new URL(url, window.location.origin);
    // cleanUrl.searchParams.delete("redirect_url");
    
    let response = await fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        }
    })
    .catch(error => {
        console.error(url, error)
    })
    if (!response)
    {
        document.getElementById('content').innerHTML = "Soft 404";
        return
    }
    switch (response.status) {
        case 403:
            console.log("Load Page", url);
            return loadPage("/login/");
        case 502:
            console.log("Load Page", url);
            window.alert("Backend error contact administrator");
            break;
        default:
            content = await response.text();
            if (response.redirected)
                url = response.url;
            console.log("Load Page", url);

            if (url === "/home/") {
                if (update_url) {
                    window.history.replaceState({ path: url, fromBack: false }, '', url);
                }
            } else {
                if (update_url) {
                    // window.history.pushState({ path: url }, '', url);
                    window.history.pushState({ path: url, fromBack: false }, '', url);
                }
            }


            document.getElementById('content').innerHTML = content;
            // Set the title based on the URL
            setTitleBasedOnURL(url);

            await loadAllScripts(originalScripts);
            checkTournament();
            execMains();
    }
}

// Function to get a cookie value by name
function getCookieValue(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Function to set the title based on the URL
function setTitleBasedOnURL(url) {
    const language = getCookieValue('language');
    // console.log("Setting title based on URL", url);
    if (url.includes("/login/")) {
        document.title = getTranslation(language, 'login');
    } else if (url.includes("register/")) {
        document.title = getTranslation(language, 'register');
    } else if (url.includes("logout/")) {
        document.title = getTranslation(language, 'logout');
    } else if (url.includes("home/")) {
        document.title = getTranslation(language, 'home');
    } else if (url.includes("tournament/")) {
        document.title = getTranslation(language, 'tournament');
    } else if (url.includes("lobby/")) {
        document.title = getTranslation(language, 'lobby');
    } else if (url.includes("settings/")) {
        document.title = getTranslation(language, 'settings');
    } else if (url.includes("loading/")) {
        document.title = getTranslation(language, 'loading');
    } else if (url.includes("game/local/select/")) {
        document.title = getTranslation(language, 'selectGame');
    } else if (url.includes("profile/")) {
        document.title = getTranslation(language, 'otherProfile');
    } else if (url.includes("/?gameType=0")) {
        if(url.includes("&render=true"))
            document.title = getTranslation(language, 'pong3D');
        else
            document.title = getTranslation(language, 'pong2D');
    }
    else if (url.includes("/?gameType=1")) {
        document.title = getTranslation(language, 'connect4');
    }
    else if (url.includes("/password/")) {
        document.title = getTranslation(language, 'password');
    }
    else if (url.includes("/game/")) {
        document.title = getTranslation(language, 'game');
    }
    else {
        document.title = getTranslation(language, 'default');
    }
}

// Translation arrays for each language
const translations = {
    en: {
        login: "Login",
        register: "Register",
        logout: "Logout",
        home: "Home",
        tournament: "Tournament",
        lobby: "Lobby",
        settings: "Settings",
        loading: "Loading",
        selectGame: "Select Game",
        otherProfile: "Other Profile",
        pong2D: "Pong 2D",
        pong3D: "Pong 3D",
        connect4: "Connect 4",
        password: "Password",
        game: "Game",
		link: "Link",
        default: "Default"
    },
    fr: {
        login: "Connexion",
        register: "S'inscrire",
        logout: "Déconnexion",
        home: "Accueil",
        tournament: "Tournoi",
        lobby: "Salon",
        settings: "Paramètres",
        loading: "Chargement",
        selectGame: "Sélectionner un jeu",
        otherProfile: "Autre profil",
        pong2D: "Pong 2D",
        pong3D: "Pong 3D",
        connect4: "Puissance 4",
        password: "Mot de passe",
        game: "Jeu",
		link: "Lier",
        default: "Défaut"
    },
    nl: {
        login: "Inloggen",
        register: "Registreren",
        logout: "Uitloggen",
        home: "Home",
        tournament: "Toernooi",
        lobby: "Lobby",
        settings: "Instellingen",
        loading: "Laden",
        selectGame: "Selecteer spel",
        otherProfile: "Ander profiel",
        pong2D: "Pong 2D",
        pong3D: "Pong 3D",
        connect4: "4 op een rij",
        password: "Wachtwoord",
        game: "Spel",
		link: "Koppelen",
        default: "Standaard"
    },
    es: {
        login: "Iniciar sesión",
        register: "Registrarse",
        logout: "Cerrar sesión",
        home: "Inicio",
        tournament: "Torneo",
        lobby: "Sala",
        settings: "Configuraciones",
        loading: "Cargando",
        selectGame: "Seleccionar juego",
        otherProfile: "Otro perfil",
        pong2D: "Pong 2D",
        pong3D: "Pong 3D",
        connect4: "Línea 4",
        password: "Contraseña",
        game: "Juego",
		link: "Enlace",
        default: "Predeterminado"
    }
};

// Function to get translation based on language and key
function getTranslation(language, key) {
    return translations[language] && translations[language][key] ? translations[language][key] : translations['en'][key];
}

window.addEventListener('popstate', (event) => {
    event.preventDefault();

    let path;
    if (event.state && event.state.path) {
        if (event.state.path[0] != "/")
            path = "/" + event.state.path;
        else
            path = event.state.path;
    } else {
        path = window.location.pathname;
    }
    console.log("Event state:", event.state);
    console.log("Resolved path:", path);

    // if (event.state && path) {
        // loadPage(path, false);
    // }
        loadPage(path, false);
});
        
const loadedScripts = new Set();
async function loadScriptOnce(src, callback) {
    if (loadedScripts.has(src)) {
        console.log('Script already loaded:', src);
        callback();
        return;
    }
    const script = document.createElement('script');
    script.src = src;
    script.type = 'text/javascript';
    script.onerror = () => {
        console.error(`Error loading script: ${src}`);
    };
    // document.head.appendChild(script);
    loadedScripts.add(src);
    callback();
    document.body.appendChild(script);
    return new Promise((resolve, reject) => { script.onload = () => resolve()})
}


async function loadAllScripts(originalScripts) {
    const scripts = document.querySelectorAll('script');
    const scriptPromises = [];

    scripts.forEach(script => {
        const scriptSrc = script.src;
        if (scriptSrc && !loadedScripts.has(scriptSrc)) {

            for (const originalScript of originalScripts) {
                if (script.getAttribute('src') === originalScript.getAttribute('src')) {
                    return;
                }
            }

            const scriptPromise = loadScriptOnce(scriptSrc, () => {
                console.log('Script loaded successfully:', scriptSrc);
                // script.remove();
            });
            scriptPromises.push(scriptPromise);

        } //else {
        //     // console.log('Script not found or already loaded: ',  scriptSrc);
        //     script.remove();
        // }
    });

    await Promise.all(scriptPromises);
}

function addMain(fnptr) {
    key = document.querySelector('[name=pageKey]').value;
    fnarray = []
    if (mains.has(key))
        fnarray = mains.get(key);
    fnarray.push(fnptr);
    mains.set(key, fnarray);
}

function execMains() {
    if (document.querySelector('[name=pageKey]'))
    {
        key = document.querySelector('[name=pageKey]').value;
        if (mains.has(key))
            mains.get(key).forEach(fnptr => fnptr());
    }
}