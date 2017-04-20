$(document).ready(function(){
    console.log('Custom menu js loaded');
    var $languageFlags = $('.language-flag');
    $languageFlags.on('click', function(e){
        var $target = $(e.target);
        var $langForm = $('#language-change-form');
        var selectedLanguage = $target.data().languageCode;
        $langForm.find('input[name=language]').val(selectedLanguage);
        $langForm.submit()
        console.log(selectedLanguage);
    })
})