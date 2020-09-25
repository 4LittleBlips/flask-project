$("#edit{{comment.id}}").click(function() {
		$.ajax({
			type: 'POST',
			url: "{{ url_for('editComment', comment_id=comment.id) }}",
			data: JSON.stringify({
				'comment_id': {{ comment.id }}
			}),
			contentType: 'application/json;charset=UTF-8',
			dataType: 'json',
			success: function(data){
				$("#comment{{comment.id}} p").text(data.edited_text)
				console.log(data);
			},
			error: function(error){
				console.log(error);
			}
		});
	});

	$("#delete{{comment.id}}").click(function() {
		$.ajax({
			type: 'DELETE',
			url: "{{ url_for('deleteComment', comment_id=comment.id) }}",
			data: JSON.stringify({comment_id: {{ comment.id }}}),
			contentType: 'application/json',
			dataType: 'json',
			beforeSend: function() {
				return confirm('Are you sure you would like to delete this comment?');
			},
			success: function(data){
				$("#comment{{comment.id}}").hide()
				console.log(data);
			},
			error: function(error){
				console.log(error);
			}
		});
	});

