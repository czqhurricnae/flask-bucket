$(function() {
	$("#btnSignUp").click(function() {
		$.ajax({
			url: "/signUp",
			data: $("form").serialize(),
			type: "POST",
			/* success: function(response) { */
								// console.log(response);
                // window.location.href = Flask.url_for('index');
		/* }, */
            success: function(jsonData) {
                var response = JSON.parse(jsonData);
                $.each(response, function(key, value){
                  if (value == "ok") {
                    window.location.href = Flask.url_for('index');
                  }
                  else {
                    window.location.href = Flask.url_for("signUp");
                }
                  if (key == "info") {
                    window.location.href = Flask.url_for("signUp");
                  }
                });
            },
			error: function(error) {
				console.log(error);
			}
		});
	});
});
