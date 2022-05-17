let updateBtn = document.getElementsByClassName("update-cart");

for (let i = 0; i < updateBtn.length; i++) {
    updateBtn[i].addEventListener("click", function () {
        const productId = this.dataset.product;
        const action = this.dataset.action;

        if (user == "AnonymousUser") {
            addCookieItem(productId, action);
            // console.log(user);
        } else {
            updateUserOrder(productId, action);
        }
    });
}

const addCookieItem = (productId, action) => {
    if (action == "add") {
        if (cart[productId] == undefined) {
            cart[productId] = { "quantity": 1 };
            // console.log('added');
        } else {
            cart[productId]["quantity"] += 1;
        }
    }

    if (action == "remove") {
        cart[productId]["quantity"] -= 1;

        if (cart[productId]['quantity'] <= 0) {
            // console.log('removed');
            delete cart[productId];
        }
    }
    // console.log('Cart: ', cart);
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain;path=/"
    location.reload();
};

const updateUserOrder = (productId, action) => {
    let url = "/update_item/";

    fetch(url, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
        },
        body: JSON.stringify({ productId: productId, action: action }),
    })
        .then((res) => {
            return res.json();
        })
        .then((data) => {
            location.reload();
        });
};
