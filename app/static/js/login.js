$(function () {

        $("#betaForm").submit(function( event ) {
          event.preventDefault();

          var $form = $( this ),
          password = $form.find("#betaPass").val(),
          username = $form.find("#betaEmail").val();

          var Data = { "password": password, "username": username };
          console.log(Data);

          var jsonData = JSON.stringify(Data);

          
          $.ajax({
            type: "POST",
            url: "/admin/",
            data: jsonData,
            contentType: "application/json; charset=UTF-8",
            dataType: "json",

            success: function() {
                console.log("Data has been posted");

                $("#alert")
                    .find("strong")
                    .empty()
                    .append("You were succcesfully logged in!");

                window.setTimeout(urlChange, 1150);

                function urlChange() {
                  document.location = "/adminTasks/";
                }

            },

            error: function() {
              console.log("Failed");
              
              $("#alert")
                  .find("strong")
                  .empty()
                  .append("Failed! Password or Username Does not Match Existing user")
            },

            always: function() {
              console.log(jsonData);
            },
            
          });

        });
});