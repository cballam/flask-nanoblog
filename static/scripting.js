// Toggles given item
function collapseItem(id){
  $(document).ready(function(){
      $(id).toggle(10);
  });
};

// Sends data to score api
function newScore(score, comment_id, post_id){
  object = {
    score: score,
    comment_id: comment_id,
    post_id: post_id
  };
  // Default to comment url
  let url = '../api/comments';
  if (object.comment_id === null){
    url = '../api/posts';
  }
  $.ajax({
        url: url,
        type: "post",
        data: object,
        success: function (response) {
          // Create typeCol object to hold values needed to change button color
          let typeCol = null;
          if (object.comment_id !== null) {
            typeCol = [comment_id, "up", "down"];
            type = ["comment", comment_id];
          }
          else {
            typeCol = [post_id ,"upPOST", "downPOST"];
            type = ["post", post_id];
          }
          // Button color toggling logic
          toggleColor(typeCol, score);
          updateScore(type, response);
        }
    });
};

function toggleColor(type, score){
   if (score == 1){
     if ($("#" + type[0] + type[1]).css('background-color') == 'rgb(0, 128, 0)'){
       $("#" +type[0]+ type[1]).css('background-color', "lightgray");
     }
     else {
       $("#" +type[0]+ type[1]).css('background-color', "green");
     }
     $("#" +type[0]+ type[2]).css('background-color', "lightgray");
   }
   else if (score == -1){
     if ($("#" +type[0]+ type[2]).css('background-color') == 'rgb(255, 0, 0)'){
       $("#" +type[0]+ type[2]).css('background-color', "lightgray");
     }
     else {
       $("#" +type[0]+ type[2]).css('background-color', 'red');
     }
     $("#" +type[0]+ type[1]).css('background-color', "lightgray");
   }
};

function updateScore(type, response){
  console.log(type);
  console.log(response.score);
  $("#" + type[0] + type[1] + "points").text(response.score);
}
