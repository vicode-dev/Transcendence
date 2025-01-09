class Tree {
    constructor(players) {
        this.players = players;
        this.length = players.length;
        this.leaves = (this.length + 1) / 2;
        this.height = Math.log(this.leaves) / Math.log(2);
        this.idx = 0;
        this.bot = this.find_bot();
    }

    find_bot() {
        let count = 0;
        for (let i = 0; i < this.leaves; i++) {
            if (this.players[i + (this.length - this.leaves)] == null)
                count++;
        }
        return count;
    }

    parent(i) {
        parent = i % 2 == 0 ? (i - 2) / 2 : (i - 1) / 2;
        if (i <= 0)
            parent = 0;
        this.idx = parent;
        return parent;
    }

    leftChild(i) {
        child = (2 * i) + 1;
        if (child > this.length)
            child = i;
        this.idx = child;
        return child;
    }

    rightChild(i) {
        child = (2 * i) + 2;
        if (child > this.length)
            child = i;
        this.idx = child;
        return child;
    }

    sibling(i) {
        sibling = i % 2 == 0 ? i - 1 : i + 1;
        if (i == 0)
            sibling = 0;
        this.idx = sibling;
        return sibling;
    }
}

function addBranch(svg, x1, y1, x2, y2) {
    let branch = document.createElementNS("http://www.w3.org/2000/svg", "line");

    branch.setAttribute("x1", x1);
    branch.setAttribute("y1", y1);
    branch.setAttribute("x2", x2);
    branch.setAttribute("y2", y2);
    branch.setAttribute("stroke", "black");
    branch.setAttribute("stroke-width", "2");
    svg.appendChild(branch);
}

function addPlayer(svg, id, x, y) {
    let player = document.createElementNS("http://www.w3.org/2000/svg", "image");
    if (id == 0) {
        // player.setAttribute("href", '/static/tournament/question_mark.jpg');
        player.setAttribute("x", x - 10);
        player.setAttribute('y', y - 10);
        player.setAttribute('width', 20);
        player.setAttribute('height', 20);
        svg.appendChild(player)
        return ;
    }
    fetch("/api/player/" + id + "/avatar/")
        .then(response => {return response.blob();
        })
        .then(blob => {
            let imgUrl = URL.createObjectURL(blob);
            player.setAttribute("href", imgUrl);
            player.setAttribute("x", x - 10);
            player.setAttribute('y', y - 10);
            player.setAttribute('width', 20);
            player.setAttribute('height', 20);
            svg.appendChild(player)

        })

}

function createTree(svg, tree, length, depth, oldbot) {
    h = 300 / ((length - tree.bot) + 1);
    w = (300 / (tree.height + 1)) * (tree.height - depth);
    for (i = 0; i < length - tree.bot; i++) {
        id = tree.players[i + length - 1];
        x = w + (300 / ((tree.height + 1) * 2));
        y = h * (length - tree.bot - i);
        if (id != null)
            addPlayer(svg, id, x, y);
        if (length < tree.leaves) {
            oldH = 300 / (2 * length - oldbot + 1)
            addBranch(svg, x, y, x - (300 / (tree.height + 1)), ((length * 2 - oldbot) - 2 * i) * oldH);
            if (((length * 2 - oldbot) % 2 == 0) || ((length * 2 - oldbot) % 2 == 1 && i < length - tree.bot - 1))
                addBranch(svg, x, y, x - (300 / (tree.height + 1)), (length * 2 - oldbot - 2 * i - 1) * oldH);
        }
    }
    if (length > 1) {
        bot = tree.bot
        tree.bot = Math.floor(tree.bot / 2);
        createTree2(svg, tree, length / 2, depth - 1, bot);
    }
}

function mainPlayersTree(pid) {
    let players = new Tree(pid);

    console.log("HI")
    console.log(players);
    let tree = document.getElementById("tree");
    tree.innerHTML = '';
    createTree(tree, players, players.leaves, players.height, 0);
}

addMain(mainPlayersTree);