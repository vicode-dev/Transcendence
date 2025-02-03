function handle_language(value) {
    document.cookie = `language=${value};SameSite=Lax`;  
    loadPage(window.location.pathname + window.location.search);
}