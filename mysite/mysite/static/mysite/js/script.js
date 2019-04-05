var filtreElts = document.getElementById("filtre");
const path = "/static/mysite/resized/";
const path_img = "/static/mysite/Images/"
const res_path_img = "/static/mysite/Result/"

//filtreElts.style.visibility = 'hidden';

var onFiltreElt = true; //permet de gérer l'affichage liste des filtres/images
var fileUploaded = false; //pas de reseau chargé par defaut
var validerFile = false;
let NNChosen = false;
let ClChosen = false;
let ImgChose = false;
var layerSelected = false; //true dès qu'on clique sur une couche

var divNNElt = document.getElementById('divNN');
divNNElt.classList.add('div-neural-network');

let path_file = "";
let classSelected = "";
let imgSelected = "";

function resetAll() {
  onFiltreElt = true; //permet de gérer l'affichage liste des filtres/images
  fileUploaded = false; //pas de reseau chargé par defaut
  validerFile = false;
  NNChosen = false;
  ClChosen = false;
  ImgChose = false;
  layerSelected = false; //true dès qu'on clique sur une couche

  path_file = "";
  classSelected = "";
  imgSelected = "";
}

function removeChildren(listName) {
  while(listName.firstChild) {
    listName.removeChild(listName.firstChild);
  }
}

function selectNetwork(tmp) {
  if(path_file === "")
  {
    NNChosen = true;
    tmp.style.fontWeight = "bold";
    path_file = tmp.textContent;
    let box = document.createElement("a");
    box.className = "dropdown-item";
    box.href = "#";
    box.textContent = path_file;
    let menu = document.getElementById("menu-net");
    removeChildren(menu);
    menu.className = "dropdown-menu";
    document.getElementById("btnGroupDrop1").textContent = tmp.textContent;
  }
}

function createItem(content) {
  let item = document.createElement("a");
  item.className = "dropdown-item";
  item.href = "#";
  item.textContent += content;
  return item;
}

function uploadfile() {
  if (NNChosen === true) {
    return;
  }
  /*Commencer par sélectionner le réseau*/
  const reqFile = new XMLHttpRequest();
  reqFile.open('GET', 'get_file/', false);
  reqFile.responseType = 'JSON'
  reqFile.send();
  //console.log(reqFile);

  /* Si un réseau est déjà chargé */
  if (NNChosen === true) {
    return;
  }

  /*On récupère la liste et demande au client de choisir*/

  let listeReseauJSon = JSON.parse(reqFile.responseText);
  let listeReseau = document.getElementById('menu-net');
  removeChildren(listeReseau);
  for (var i in listeReseauJSon) {
    let tmp = createItem(listeReseauJSon[i]);
    listeReseau.appendChild(tmp);
    tmp.addEventListener('click', function(){
      selectNetwork(tmp);
    })

  }
  document.getElementById("menu-net").className = "dropdown-menu show";
}


document.querySelector("#btnGroupDrop1").addEventListener('click', uploadfile);

function resetFilters() {
  let filterTable = document.getElementById("tableFilters");
  removeChildren(filterTable);
  let tableColGrp = document.createElement("colgroup");
  tableColGrp.className = "columns";
  filterTable.appendChild(tableColGrp);
}

function resetHeatMap() {
  let heatMapBox = document.getElementById("heatMapBox");
  removeChildren(heatMapBox);
}

function resetNet() {
  if (NNChosen === true) {
    NNChosen = false;
    removeChildren(document.getElementById("divNN"));

    const reqNNReset = new XMLHttpRequest();
    reqNNReset.open("POST", "reset_nn/", false);
    reqNNReset.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    reqNNReset.send();

    let classes = document.getElementById("classToolBar");
    let cells = document.getElementById("filecell");
    cells.removeChild(classes);
    if (ClChosen) {
      cells.removeChild(document.getElementById('validerImg'));
      if (ImgChose) {
        //cells.removeChild(document.getElementById("imgSelectedName"));
        cells.removeChild(document.getElementById("img-selected"));
        if (layerSelected) {
          resetFilters();
          resetHeatMap();
        }
      }
    }
    resetAll();
  }
}

document.getElementById("removeNet").addEventListener('click', resetNet);

function insertImg(tmp){
  if(imgSelected === "")
  {
    ImgChose = true;
    tmp.style.fontWeight = "bold";
    tmp.id = "imgSelectedName";
    imgSelected = tmp.textContent;
    let box = document.querySelector("#filecell");
    box.removeChild(document.querySelector("#listeImg"));
    let selected = document.createElement('img');
    selected.src = path_img + imgSelected;
    selected.classList.add('class_mini');
    selected.id = 'imgSelectedMini';
    let btn = document.querySelector('#validerImg')
    box.insertBefore(selected, btn);
  }
}

function okImg() {
  if ((imgSelected != "") && (ImgChose === true))
  {
    //ImgChosen = false;
    document.querySelector('.class_mini').remove();
    const reqImgChosen = new XMLHttpRequest();
    reqImgChosen.open('POST', 'img_selected/', false);
    reqImgChosen.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    reqImgChosen.send("img="+imgSelected + '&cl=' + classSelected);
    console.log("image choisie : " + imgSelected);
    let answer = JSON.parse(reqImgChosen.responseText);
    let miniature = document.createElement('img');
    miniature.id = 'img-selected';
    //console.log(answer.img);
    miniature.src = "";
    let chemin = path_img + answer.img;
    miniature.src =  chemin;
    console.log(chemin)
    miniature.classList.add("miniature");
    document.querySelector('#filecell').appendChild(miniature);
    document.getElementById('validerImg').disabled=true;
  }
}

function resetClass() {
  console.log('miboundhbqzdj')
  if ((classSelected != "") && (ClChosen === true))
  {
    classChosen = false;
    ClSelected = "";
    imgSelected = "";
    ImgChosen = false;
    ClChosen = false;
    if ((document.querySelector('#listeImg')) != null)
      document.querySelector('#filecell').removeChild(document.querySelector('#listeImg'));


    if ((document.querySelector('#imgSelectedMini')) != null)
     document.querySelector('#filecell').removeChild(document.querySelector('#imgSelectedMini'));

   if ((document.querySelector('#img-selected')) != null)
     document.querySelector('#filecell').removeChild(document.querySelector('#img-selected'));


   document.querySelector('#filecell').removeChild(document.querySelector('#validerImg'));

   document.getElementById('validerClass').disabled=false;

   console.log('class unselected');
 }
}

function okClass(classSelected, ClChosen) {
  if ((classSelected != "") && (ClChosen === true))
  {

    ClChosen = false;
    const reqClChosen = new XMLHttpRequest();
    reqClChosen.open('POST', 'get_img/',false);
    reqClChosen.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    reqClChosen.send("cl=" + classSelected);

    console.log('classe choisie : ' + classSelected);

    let listeImgJSon = JSON.parse(reqClChosen.responseText);
    let listeImg = document.createElement('div');
    listeImg.id = "listeImg";
    listeImg.classList.add("div-liste-img");
    for (var i in listeImgJSon)
    {
      let tmp = document.createElement('img');
      tmp.src += path_img + listeImgJSon[i];
      tmp.textContent += listeImgJSon[i];
      tmp.classList.add('class_mini');
      listeImg.appendChild(tmp);
      tmp.addEventListener('click', function() {
        insertImg(tmp);
      });

    }
    document.querySelector("#filecell").appendChild(listeImg);


    let btnValiderImg = document.createElement('input');
    btnValiderImg.type = "button"
    btnValiderImg.id = 'validerImg';
    btnValiderImg.value = 'Valider image'
    btnValiderImg.name = 'Valider image'
    btnValiderImg.className='btn btn-primary'
    btnValiderImg.addEventListener('click', okImg);
    document.querySelector('#filecell').appendChild(btnValiderImg);
  }
}

function onSelectClass(item, classSet) {
  ClChosen = true;
  classSelected = item.textContent;
  classSet.className = "dropdown-menu";
  document.getElementById("classBtn").textContent = item.textContent;
  removeChildren(classSet);
}

function createClassBtnGrp(classSet) {
  if (ClChosen === true) {
    {
     console.log('test');
     return;
   }
 }
 const reqCl = new XMLHttpRequest();
 reqCl.open('GET', 'get_cl/', false);
 reqCl.responseType = 'JSON'
 reqCl.send();
 let listeClassJSon = JSON.parse(reqCl.responseText);
 removeChildren(classSet);
 for (var i in listeClassJSon) {
  let item = createItem(listeClassJSon[i]);
  classSet.appendChild(item);
  item.addEventListener('click', function() {
    onSelectClass(item, classSet);
  });
}
classSet.className = "dropdown-menu show";
}

function createOkIcon() {
  let okIcon = document.createElement("span");
  okIcon.className = "fas fa-check";
  okIcon.textContent = "Ok";
  return okIcon;
}

function createRemove() {
  let timeIcon = document.createElement("span");
  timeIcon.className = "fas fa-times";
  return timeIcon;
}

function okFile() {
  if ((path != "") && (NNChosen === true))
  {
    //NNChosen = false;
    const req = new XMLHttpRequest();
    req.open('POST', 'valider/', false);
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    req.send("net="+path_file);
    console.log("reseau choisi : " + path_file);

    console.log(req.responseText)

    /*let NNElt = document.createElement("div");
    NNElt.id = "NNElt";
    NNElt.classList.add('neural-network');*/
    divNNElt.classList.add('neural-network');
    validerFile = true;

    let reqAsw = JSON.parse(req.responseText);
    let layerSTR = reqAsw.architecture;

    computeNN(layerSTR, divNNElt);

    /* Group of buttons to contain buttons */
    let btnGrp = document.createElement("div");
    btnGrp.className = "btn-group";
    btnGrp.id = "btn-class-grp";

    /* affichage du bouton de choix de classe */
    let toolbar = document.createElement("div");
    toolbar.className = "btn-toolbar";
    toolbar.role = "toolbar";
    toolbar.id = "classToolBar";
    let classMenu = document.createElement("div");
    classMenu.id = "class-menu";
    classMenu.className = "btn-group";
    classMenu.role = "group";
    /* Le bouton */
    let classBtn = document.createElement('button');
    classBtn.textContent = "Choisir la classe";
    classBtn.id = 'classBtn';
    classBtn.className = "btn btn-primary dropdown-toggle";
    classBtn.type = 'button';
    /* Le menu defilant */
    let classSet = document.createElement("div");
    classSet.className = "dropdown-menu";
    classSet.id = "menu-class";
    /* Reset button */
    let classResetBtn = document.createElement('button');
    classResetBtn.id = 'classResetBtn';
    //classResetBtn.className = "btn btn-primary dropdown-toggle";
    classResetBtn.type = 'button';
    classResetBtn.classList.add("btn")
    classResetBtn.classList.add("btn-danger");
    classResetBtn.appendChild(createRemove());


    classMenu.appendChild(classSet);
    classMenu.appendChild(classBtn);
    toolbar.appendChild(classMenu);
    toolbar.appendChild(classResetBtn);

    /* ajout du traitement de la requete de demande des classes*/
    classBtn.addEventListener('click', function () {
      createClassBtnGrp(classSet);
    });

    classResetBtn.addEventListener('click', resetClass);


    /* affiche le boutton de validation de classe */
    let validerClass = document.createElement('button');
    validerClass.id = 'validerClass';
    validerClass.className = "btn btn-success";
    validerClass.appendChild(createOkIcon());

    validerClass.addEventListener('click', function() {
     okClass(classSelected, ClChosen);
     document.getElementById('validerClass').disabled=true;
   })
    document.querySelector('#filecell').appendChild(toolbar);
    toolbar.appendChild(classMenu);
    toolbar.appendChild(validerClass);
  }
}

document.querySelector("#validerFile").addEventListener('click', okFile);

//document.querySelector("#btnSwitchFiltre").addEventListener('change', switchBtn);



function zoom()
//permet d'effectuer un zoom sur l'instance qui appelle la fonction
{
  this.classList.remove("dezoom");
  this.classList.add("zoom");
}

function dezoom()
//permet d'effectuer un dezoom sur l'instance qui appelle la fonction
{
  this.classList.remove("zoom");
  this.classList.add("dezoom");
}

function objToArray(obj) {
  res = [];
  for (elt in obj) {
    res.push(obj[elt]);
  }
  return res;
}

function createLineImgs(path, arrName, i, mult, colMax) {
  let line = document.createElement('tr');
  for (let col = 0; col < colMax; col ++) {
    let elt = document.createElement("td");
    let value = document.createElement('img');
    value.src = path + arrName[i * mult + col];
    value.alt = "Responsive image";
    value.classList.add("filter");
    elt.appendChild(value);
    line.appendChild(elt);
  }
  return line;
}

function computeFiltre_aux(filters)
//calcule les filtres de la couche c
{
  let tableFilters = document.getElementById("tableFilters");
  let filtersList = objToArray(filters);
  let nbLignes = filtersList.length / 3;
  for(let i = 0; i < nbLignes - 1; i++) {
    let line = createLineImgs(res_path_img, filtersList, i, 3, 3);
    tableFilters.appendChild(line);
  }
  /* Add potential last images */
  let line = createLineImgs(res_path_img, filtersList, nbLignes - 1, 3, filtersList.length % 3);
  tableFilters.appendChild(line);
}

function computePic(path)
{
  let imgElt = document.createElement('img');
  imgElt.src = path;
  return imgElt;
}


function zoom_big()
{
  this.classList.remove('dezoom-img');
  this.classList.add('zoom-img');
}

function dezoom_big()
{
  this.classList.remove('zoom-img');
  this.classList.add('dezoom-img');
}


function switchBtn()
{
  var box = document.getElementById('filtreBox');

  if (layerSelected === true)
  {

    if (onFiltreElt === true)
    {
      if (box.children.length > 0)
        box.removeChild(box.children[1]);
      let img = computePic(path + "test.jpg");
      /*img.addEventListener('mouseover', zoom_big);
      img.addEventListener('mouseout', dezoom_big);*/
      img.style = "zoom";
      box.style.overflow = 'visible';
      box.appendChild(img);
      onFiltreElt = false;
    }
    else
    {
      box.removeChild(box.children[1]);
      box.style.overflow = 'auto';
      computeFiltre_aux();
      onFiltreElt = true;
    }
  }
  else
  {
    //box.children[1].textContent =''; //si aucune couche n'est selectionnée, laisser l'espace vide
  }
  /*let label = document.createElement('p');
  label.id = 'nomBtnFiltre';
  label.textContent = 'Filtres/Image';
  document.getElementById('filtreBox').appendChild(label);//document.getElementById('nomBtnFiltre').textContent = 'Filtres/Image';
  */
}



function newRectangle(id)
{
  var rectangle = document.createElement('p');
  rectangle.addEventListener('click', function(){
    computeFiltre(id);
  }) //passer en argument les filtres de la couche en question
  return rectangle;
}


/*document.getElementById('closeFiltre').style.visibility = 'hidden';
document.getElementById('closeFiltre').addEventListener('click', function() {
  this.style.visibility = 'hidden';
  document.getElementById('filtreBox').children[1].remove();
  document.querySelector("#NNElt").remove();
  layerSelected = false;
  validerFile = false;
})*/

/* Architecture of the network */
const classAssoc = {
  i : "input", f : "flatten", c : "convolution", p : "pooling", d : "dense"
}

const boxName = {
  i : "input", f : "flat", c : "conv", p : "pool", d : "dense"
};

let layerArchi = "";

function displayHeatMap(heatMap) {
  let heatMapBox = document.getElementById("heatMapBox");
  removeChildren(heatMapBox);
  let newImg = document.createElement("img");
  heats = objToArray(heatMap);
  newImg.src = res_path_img + heats[0];
  newImg.alt = "Responsive image";
  newImg.classList.add("heatMap");
  heatMapBox.appendChild(newImg);
}

function computeFiltre(layer_id)
{
  if (layerArchi[layer_id] !== "c") {
    alert("La couche sélectionnée n\'est pas une couche convolutionnelle.");
    return;
  }

  let heatMapBox = document.querySelector('#heatMapBox');
  while (heatMapBox.firstChild) {
    heatMapBox.removeChild(heatMapBox.firstChild);
  }
  if (!ImgChose) {
    alert("Aucune image n\'a été sélectionné, lancement de filter_max sur la couche" + layer_id);
    document.querySelector('#loader').style.visibility = "visible";
    let req = new XMLHttpRequest();
    req.open('POST', 'filter_max/', false);
    req.responseType = 'JSON'
    req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    console.log("layer="+layer_id);
    req.send("layer="+layer_id);
    if (req.status === 200)
    {
      listeFiltres = JSON.parse(req.responseText)
      console.log(listeFiltres);
      computeFiltre_aux(listeFiltres.filters);
      displayHeatMap(listeFiltres.heatMap);

      console.log('done')
      layerSelected = true;
      document.querySelector('#loader').style.visibility = "hidden";
    }
    return;
  }
  let e = document.getElementById('tableFilters');
  if(e.children.length > 1)
  {
    let tmp = e.children[0];
    while (e.firstChild) {
      e.removeChild(e.firstChild);
    }
    e.appendChild(tmp);
  }
  /* Create a request
  to compute result filters*/

  //document.querySelector('#test').textContent = "loading, please wait ...";

  //document.querySelector('#loader').style.visibility = "visible";

  let loader = document.createElement("div");
  loader.classList.add("loader");
  e.appendChild(loader);
  let loader2 = loader.cloneNode();
  loader2.classList.add("loader");

  heatMapBox.appendChild(loader2);

  let req = new XMLHttpRequest();
  req.open('POST', 'get_filters/', false);
  req.responseType = 'JSON'
  req.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
  console.log("layer="+layer_id);
  req.send("layer="+layer_id);
  e.removeChild(loader);

  if (req.status === 200)
  {
    listeFiltres = JSON.parse(req.responseText)
    console.log(listeFiltres);
    computeFiltre_aux(listeFiltres.filters);
    displayHeatMap(listeFiltres.heatMap);

    console.log('done')
    layerSelected = true;
  }
}

function computeClass(classId, i) {
  tmp = newRectangle(i);
  tmp.textContent = boxName[classId];
  tmp.classList.add(classAssoc[classId] + '-layer');
  return tmp;
}

function drawLineBack(i, mult, colMax) {
  let line = document.createElement('tr');
  /* Reversed-X Arrow */
  let elt = document.createElement("td");
  elt.colSpan = "11";
  let reverse90Arrow = document.createElement('img');
  reverse90Arrow.src = path + "fleche.png";
  reverse90Arrow.classList.add('arrow-reverse-XY');
  //reverse90Arrow.style.width = (15*4*(colMax-1)).toString().concat("%");
  elt.appendChild(reverse90Arrow);
  line.appendChild(elt);
  return line;
}

function drawLineNet(layerSTR, i, mult, colMax, end) {
  let line = document.createElement('tr');
  for (let col = 0; col < colMax && i * mult + col < end; col ++) {
    let elt = document.createElement("td");
    /* Append a case */
    let classId = layerSTR[i * mult + col];
    let rect = computeClass(classId, i * mult + col);
    elt.appendChild(rect);
    line.appendChild(elt);
    /* Append an arrow */
    if (col != colMax - 1 && i * mult + col != end - 1) {
      elt = document.createElement("td");
      let arrow = document.createElement('img');
      arrow.src = path + "Arrow_right.svg.png";
      arrow.classList.add('arrow');
      elt.appendChild(arrow);
      line.appendChild(elt);
    }
  }
  return line;
}

function computeNN(layerSTR, emplacement)
{
  layerArchi = layerSTR;
  let mult = 6;
  let table = document.createElement('table');
  table.style.maxWidth = "100%";
  for (var i = 0; i < layerSTR.length/mult; i++) {
    let line = drawLineNet(layerSTR, i, mult, mult, layerSTR.length);
    //emplacement.appendChild(line);
    table.appendChild(line);
    if (i < layerSTR.length/mult - 1) {
      line = drawLineBack(i, mult, mult);
      //emplacement.appendChild(line);
      table.appendChild(line);
    }
  }
  emplacement.appendChild(table);
}

