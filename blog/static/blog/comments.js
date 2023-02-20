function createCommentElement(comment) {
    const row = document.createElement('div');
    row.className = 'row border-bottom border-3 mb-3';
    
    const col = document.createElement('div');
    col.className = 'col-12 mb-2 comment_header';
    
    const col2 = document.createElement('div');
    col2.className = 'col-12 mb-2';
    col2.textContent = comment.fields.comment;
    
    const img = document.createElement('img');
    img.className = 'img-thumbnail me-1 mt-1 mb-1';
    img.setAttribute('width', 40);
    img.setAttribute('height', 40);
    img.setAttribute('src', '/static/blog/person-bounding-box.svg');
    img.setAttribute('alt', 'Profile picture');
    
    const username = document.createElement('span');
    username.textContent = comment.fields.username;
    username.className = 'me-2'

    const dateSpan = document.createElement('span')
    const dateTime = getLocalDateTimeString(comment.fields.submit_date)
    dateSpan.textContent = `${dateTime.date} at ${dateTime.time}`
    dateSpan.className = 'comment_date'

    col.append(img, username, dateSpan);
    row.append(col, col2);

    return row;
};

function setBtnLoading(button) {
    const span = document.createElement('span');
    span.className = 'spinner-border spinner-border-sm';
    span.setAttribute('role', 'status');
    span.setAttribute('aria-hidden', 'true');

    button.append(span);
    button.disabled = true;
    button.textContent = 'Loading...';
};

function setBtnDefault(button) {
    button.innerHtml = '';
    button.disabled = false;
    button.textContent = 'Submit';
};

fetch(window.location + 'comments/')
    .then(response => response.json())
    .then(data => {
        comments = JSON.parse(data)
        comments_count = document.getElementById('comments_count');
        comments_count.textContent = comments.length
        comments.forEach(comment => {
            container = document.getElementById('comments');
            container.append(createCommentElement(comment))
        });
    });

function submitComment() {
    const comment_submit_btn = document.getElementById('comment_submit');
    comment_input = document.getElementById('comment_input');
    comment_text = comment_input.value.trim();
    
    if (!comment_text) return;

    form = new FormData();
    form.append('comment', comment_text);
    
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const options = {
        method: 'POST',
        body: form,
        headers: {'X-CSRFToken': csrftoken},
        mode: 'same-origin'
    };
    setBtnLoading(comment_submit_btn)
    
    fetch(window.location + 'comments/', options)
        .then(response => {
            setBtnDefault(comment_submit_btn);

            if (response.status === 200) {
                return response.json()
            } else {
                alert('Error: Something went wrong. Please try again later.');
            }
        })
        .then(data => {
            comment = JSON.parse(data)[0];
            container = document.getElementById('comments');
            container.append(createCommentElement(comment))
            comment_input.value = '';
        });
};

const comment_submit_btn = document.getElementById('comment_submit');
comment_submit_btn.addEventListener('click', submitComment);