odoo.define('taxsurety_website_snippet.typing_snippet', function(require) {
'use strict';
    var PublicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var qweb = core.qweb;
    var TypingSnippet = PublicWidget.Widget.extend({
        selector: '#typing_snippet',
        start:  function() {
//            console.log('typing snippet', this.$el.find("we-input[data-name='first']");

            const dynamicText = this.$el.find("h1 #typing_snippet_span")[0];
//            console.log('dt', dynamicText);
            const words = ["Love", "like Art"];

            // Variables to track the position and deletion status of the word
            let wordIndex = 0;
            let charIndex = 0;
            let isDeleting = false;

            const typeEffect = () => {
                const currentWord = words[wordIndex];
                const currentChar = currentWord.substring(0, charIndex);
                dynamicText.textContent = currentChar;
                dynamicText.classList.add("stop-blinking");

                if (!isDeleting && charIndex < currentWord.length) {
                    // If condition is true, type the next character
                    charIndex++;
                    setTimeout(typeEffect, 200);
                } else if (isDeleting && charIndex > 0) {
                    // If condition is true, remove the previous character
                    charIndex--;
                    setTimeout(typeEffect, 100);
                } else {
                    // If word is deleted then switch to the next word
                    isDeleting = !isDeleting;
                    dynamicText.classList.remove("stop-blinking");
                    wordIndex = !isDeleting ? (wordIndex + 1) % words.length : wordIndex;
                    setTimeout(typeEffect, 1200);
                }
            }

            typeEffect();
        }
    })
    PublicWidget.registry.typing_snippet = TypingSnippet;
});