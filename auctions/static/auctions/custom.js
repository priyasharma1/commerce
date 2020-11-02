document.addEventListener('DOMContentLoaded', function() {
  if (document.querySelector('#watch') != null) {
   document.querySelector('#watch').addEventListener('click', (event) => watch());
  }

  var likes = document.querySelectorAll('.removeComment');
  if (likes != null) {
    likes.forEach((element) => {
       element.addEventListener('click', (event) => delete_comment());
    })
  }
//
//  var edits = document.querySelectorAll('.edit');
//  edits.forEach((element) => {
//     element.addEventListener('click', (event) => edit_post());
//  })
});

function watch() {
  var target = this.event.target;
  var id = target.dataset.id;
    fetch("/watch/" + id, {
      method: "POST",
      body: JSON.stringify({"value" : target.dataset.value})
    })
    .then(response => {
        if (target.dataset.value === 'Y') {
          document.querySelector('#watch').textContent = "Watching";
          document.querySelector('#watch').dataset.value = "N";
          document.querySelector('#watch').classList.add('badge-secondary');
        } else {
          document.querySelector('#watch').textContent = "Add to Watchlist";
          document.querySelector('#watch').dataset.value = "Y";
          document.querySelector('#watch').classList.remove('badge-secondary');
        }
    })
}

function delete_comment() {
  element = this.event.target
  id = element.dataset.id
     fetch("/comment/" + id, {
        method: "POST"
      })
      .then(response => {
          element.closest(".card").remove();
      })

}
