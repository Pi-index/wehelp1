document.addEventListener("DOMContentLoaded", function () {
    const url = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1";
    fetch(url)
        .then(response => response.json())
        .then(data => {
            const spots = data.data.results;
            renderSpots(spots);
        })
        .catch(error => console.error("Error fetching data:", error));
});

function renderSpots(spots) {
    const smallBoxes = document.querySelector(".small-boxes");
    const bigBox = document.querySelector(".big-box");

    // 清空現有內容
    while (smallBoxes.firstChild) {
        smallBoxes.removeChild(smallBoxes.firstChild);
    }
    while (bigBox.firstChild) {
        bigBox.removeChild(bigBox.firstChild);
    }

    // 渲染前 3 個景點到 small-boxes
    for (let i = 0; i < 3 && i < spots.length; i++) {
        const spot = spots[i];
        const smallBox = createSmallBox(spot, i); // 傳入索引值（從 0 開始）
        smallBoxes.appendChild(smallBox);
    }

    // 渲染接下來的 10 個景點到 big-box
    for (let i = 3; i < 13 && i < spots.length; i++) {
        const spot = spots[i];
        const bigBoxItem = createBigBoxItem(spot, i - 3); // 傳入索引值（從 0 開始）
        bigBox.appendChild(bigBoxItem);
    }
}

function createSmallBox(spot, index) {
    const smallBox = document.createElement("div");
    smallBox.className = `small-box${(index % 3) + 1}`; // 按照順序分配 small-box1, small-box2, small-box3

    const img = document.createElement("img");
    img.src = getFirstImageUrl(spot.filelist);
    img.alt = spot.stitle;

    const text = document.createElement("div");
    text.className = "text";
    text.textContent = spot.stitle;

    smallBox.appendChild(img);
    smallBox.appendChild(text);

    return smallBox;
}

function createBigBoxItem(spot, index) {
    const gridItem = document.createElement("div");
    gridItem.className = `grid-item${(index % 10) + 1}`; // 按照順序分配 grid-item1 到 grid-item10

    const img = document.createElement("img");
    img.src = getFirstImageUrl(spot.filelist);
    img.alt = spot.stitle;

    const star = document.createElement("span");
    star.className = "star";
    star.textContent = "★";

    const titleBlock = document.createElement("div");
    titleBlock.className = "title-block";
    titleBlock.textContent = spot.stitle;

    gridItem.appendChild(img);
    gridItem.appendChild(star);
    gridItem.appendChild(titleBlock);

    return gridItem;
}

function getFirstImageUrl(filelist) {
    if (filelist) {
        const firstImageUrl = filelist.split("https://")[1];
        return `https://${firstImageUrl}`;
    }
    return "";
}