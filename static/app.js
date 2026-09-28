const products = [
    {
        id: 1,
        name: "Burger Dulce",
        price: "$1500",
        image: "img/dessert_burger_1786462447266.png"
    },
    {
        id: 2,
        name: "Pancho Mágico",
        price: "$1200",
        image: "img/dessert_hotdog_1786462456214.png"
    },
    {
        id: 3,
        name: "Pizza Pastel",
        price: "$1800",
        image: "img/dessert_pizza_1786462490716.png"
    }
];

let currentIndex = 0;

const mainImage = document.getElementById('mainImage');
const mainPrice = document.getElementById('mainPrice');
const prevBtn = document.getElementById('prevBtn');
const nextBtn = document.getElementById('nextBtn');
const mainProductLink = document.getElementById('mainProductLink');
const productGrid = document.getElementById('productGrid');

function updateCarousel() {
    mainImage.src = products[currentIndex].image;
    mainImage.alt = products[currentIndex].name;
    mainPrice.textContent = products[currentIndex].price;
}

prevBtn.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + products.length) % products.length;
    updateCarousel();
});

nextBtn.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % products.length;
    updateCarousel();
});

mainProductLink.addEventListener('click', () => {
    alert(`Te llevamos al detalle del producto: ${products[currentIndex].name}`);
});

function renderGrid() {
    productGrid.innerHTML = '';
    products.forEach(product => {
        const card = document.createElement('div');
        card.className = 'product-card';
        card.innerHTML = `
            <img src="${product.image}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p>${product.price}</p>
        `;
        card.addEventListener('click', () => {
            alert(`Abriendo: ${product.name}`);
        });
        productGrid.appendChild(card);
    });
}

// Initial render
updateCarousel();
renderGrid();
