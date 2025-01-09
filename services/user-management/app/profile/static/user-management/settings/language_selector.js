function handle_language(value) {
    document.cookie = `language=${value}`;  
    loadPage(window.location.pathname + window.location.search);
}