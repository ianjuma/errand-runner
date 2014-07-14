(function() {
	Handlebars.registerHelper('list', function(items, options) {
        var out = "<ul>";

        for (var i = 0, l = items.length; i<l; i++) {
            out = out + "<li>" + options.fn(items[i]) + "</li>";
        };

        return out + "</ul>";
	});

    var source   = $("#entry-template").html();
    var template = Handlebars.compile(source);

    var context =
        { title: "My New Post", 
                body: "This is my first post!",
        social: [
        {
          site: "Twitter",
          name: "Jack_Franklin"
        },
        {
          site: "Github",
          name: "jackfranklin"
        }
        ],
        people: [
            {firstName: "Yehuda", lastName: "Katz"},
            {firstName: "Carl", lastName: "Lerche"},
            {firstName: "Alan", lastName: "Johnson"}
        ]
    };

    
    $('.entry').append(template(context));
})(); 
//self invoking func