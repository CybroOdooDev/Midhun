odoo.define('txs_soar.rss_feed', function(require) {
'use strict';
    var PublicWidget = require('web.public.widget');
    var rpc = require('web.rpc');
    var core = require('web.core');
    var qweb = core.qweb;
    var RssFeed = PublicWidget.Widget.extend({
        selector: '.snippet_rss',
        start:  function(ev, data) {
            var el_a = this.$el.find("a");
            const RSS_URL = el_a.attr('href');
            var contentsDiv = this.$el.find('.rss_feed_contents');
            contentsDiv.empty();
            if (RSS_URL){
                $.ajax(RSS_URL, {
                    accepts:{
                        xml:"application/rss+xml"
                    },
                    dataType:"xml",
                    success:function(data) {
                        $(data).find("item").each(function () {
                            var el = $(this);
                            contentsDiv.append($('<div> <a href="'+ el.find("link").text()+ '">'+ el.find("title").text() + '</div>'));
                        });
                    }
                });
            }
        }
    })
    PublicWidget.registry.rss_feed = RssFeed;
});