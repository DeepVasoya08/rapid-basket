let wishlist = document.getElementsByClassName("update-wishlist");

for (let i = 0; i < wishlist.length; i++) {
    wishlist[i].addEventListener("click", function () {
        const productId = this.dataset.product;
        const action = this.dataset.action;

        if (user == "AnonymousUser") {
            console.log(user);
        } else {
            updateWishlist(productId, action);
        }
    });
}

const updateWishlist = (productId, action) => {
    const url = "/update_wishlist/";

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
        .then(() => location.reload());
};
