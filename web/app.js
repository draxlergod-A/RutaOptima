// Lógica de la página: manda los parámetros al servidor (app.py), recibe las rutas y las dibuja.
"use strict";

const COLORES = ["#2457d6", "#e8590c", "#2f9e44", "#ae3ec9", "#0c8599", "#c92a2a", "#5f3dc4",
  "#e67700", "#087f5b", "#a61e4d", "#1864ab", "#862e9c", "#5c940d", "#d9480f", "#364fc7"];
const ZONAS_FONDO = ["#dbe4ff", "#ffe8cc", "#d3f9d8", "#f3d9fa", "#c5f6fa", "#ffe3e3", "#e5dbff",
  "#fff3bf", "#c3fae8", "#ffdeeb"];
const $ = (id) => document.getElementById(id);
let datos = null;   // última respuesta del servidor

// ---- controles ------------------------------------------------------------------------
for (const id of ["n", "vehiculos", "k"]) {
  $(id).addEventListener("input", () => { $("o-" + id).textContent = $(id).value; });
}
// al cambiar n se sugiere una cantidad de vehículos (1 cada 7 clientes, como en el código)
$("n").addEventListener("input", () => {
  const v = Math.max(2, Math.min(15, Math.ceil(Number($("n").value) / 7)));
  $("vehiculos").value = v; $("o-vehiculos").textContent = v;
});
$("formulario").addEventListener("submit", (e) => { e.preventDefault(); calcular(); });
$("otra").addEventListener("click", () => { $("semilla").value = Math.floor(Math.random() * 10000); calcular(); });
$("ver-zonas").addEventListener("change", dibujarMapas);
$("sel-estrategia").addEventListener("change", dibujarDetalle);
document.querySelectorAll(".pestana").forEach((b) => b.addEventListener("click", () => {
  document.querySelectorAll(".pestana").forEach((x) => x.classList.toggle("activa", x === b));
  document.querySelectorAll(".vista").forEach((v) => { v.hidden = v.id !== b.dataset.pestana; });
  if (b.dataset.pestana === "experimentos") cargarGraficos();
}));

// ---- llamada al servidor --------------------------------------------------------------
async function calcular() {
  const boton = $("calcular");
  boton.disabled = true; boton.textContent = "Calculando…";
  try {
    const respuesta = await fetch("/api/resolver", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        n: Number($("n").value), vehiculos: Number($("vehiculos").value), k: Number($("k").value),
        semilla: Number($("semilla").value), distritos: $("distritos").checked,
      }),
    });
    const json = await respuesta.json();
    if (!respuesta.ok) throw new Error(json.error || "Error del servidor");
    datos = json;
    $("estado").hidden = true; $("contenido").hidden = false;
    dibujarTodo();
  } catch (error) {
    $("estado").hidden = false; $("estado").className = "aviso error";
    $("estado").textContent = "No se pudo calcular: " + error.message;
    $("contenido").hidden = true;
  } finally {
    boton.disabled = false; boton.textContent = "Calcular rutas";
  }
}

function dibujarTodo() { dibujarResumen(); dibujarTabla(); dibujarMapas(); dibujarDetalle(); }

// ---- comparación ----------------------------------------------------------------------
const NOMBRES = { voraz: "Voraz", dc_pd: "Divide y vencerás + PD" };
const FILAS = [
  ["Costo total (S/)", "costo", "menor", (v) => v.toFixed(2)],
  ["Distancia (km)", "km", "menor", (v) => v.toFixed(1)],
  ["Horas de operación", "horas", "menor", (v) => v.toFixed(1)],
  ["Vehículos usados", "vehiculos", "menor", (v) => v],
  ["Clientes atendidos", "atendidos", "mayor", (v) => v],
  ["% atendidos", "pct", "mayor", (v) => v.toFixed(1) + " %"],
  ["Tiempo de cálculo (s)", "segundos", "menor", (v) => v.toFixed(4)],
];

function dibujarResumen() {
  const a = datos.resultados.voraz.metricas, b = datos.resultados.dc_pd.metricas;
  const i = datos.instancia;
  const costoPorCliente = (m) => m.atendidos ? m.costo / m.atendidos : Infinity;
  const mejor = costoPorCliente(b) <= costoPorCliente(a) ? "Divide y vencerás + PD" : "Voraz";
  let html = `<b>${i.n}</b> clientes · <b>${i.vehiculos}</b> vehículos · k = <b>${i.k}</b> · semilla ${i.semilla}.<br>`;
  html += `Menor <b>costo por cliente atendido</b>: <b>${mejor}</b> `
    + `(S/ ${costoPorCliente(a).toFixed(2)} voraz vs. S/ ${costoPorCliente(b).toFixed(2)} D&amp;V+PD). `
    + `Atendidos: ${a.pct} % vs. ${b.pct} %.`;
  for (const [nombre, r] of Object.entries(datos.resultados)) {
    if (!r.valida) html += `<br><span class="mal">⚠ ${NOMBRES[nombre]} no es válida: ${r.errores[0]}</span>`;
  }
  $("ganador").innerHTML = html;
}

function dibujarTabla() {
  const a = datos.resultados.voraz, b = datos.resultados.dc_pd;
  let html = "<thead><tr><th>Métrica</th><th>Voraz</th><th>Divide y vencerás + PD</th></tr></thead><tbody>";
  for (const [etiqueta, clave, sentido, formato] of FILAS) {
    const x = a.metricas[clave], y = b.metricas[clave];
    const empate = x === y;
    const mejorX = !empate && (sentido === "menor" ? x < y : x > y);
    html += `<tr><td>${etiqueta}</td><td class="${!empate && mejorX ? "mejor" : ""}">${formato(x)}</td>`
      + `<td class="${!empate && !mejorX ? "mejor" : ""}">${formato(y)}</td></tr>`;
  }
  html += `<tr><td>Cumple todas las restricciones</td><td>${a.valida ? "✔" : "✘"}</td><td>${b.valida ? "✔" : "✘"}</td></tr></tbody>`;
  $("tabla-comparacion").innerHTML = html;
}

// ---- mapas SVG ------------------------------------------------------------------------
function dibujarMapas() {
  dibujarMapa("mapa-voraz", "titulo-voraz", "voraz");
  dibujarMapa("mapa-dcpd", "titulo-dcpd", "dc_pd");
}

function dibujarMapa(idMapa, idTitulo, clave) {
  const res = datos.resultados[clave], inst = datos.instancia;
  $(idTitulo).textContent = `${NOMBRES[clave]} — S/ ${res.metricas.costo.toFixed(2)} · ${res.metricas.vehiculos} veh. · ${res.metricas.pct} % atendidos`;
  const L = inst.area_km, M = 0.8, vista = `${-M} ${-M} ${L + 2 * M} ${L + 2 * M}`;
  const px = (x) => x, py = (y) => L - y;               // el eje y crece hacia arriba
  const porId = {}; inst.clientes.forEach((c) => { porId[c.id] = c; });
  const noAtendidos = new Set(res.no_atendidos);
  let svg = `<svg viewBox="${vista}" xmlns="http://www.w3.org/2000/svg">`;
  svg += `<rect x="0" y="0" width="${L}" height="${L}" fill="none" stroke="#9aa4bd" stroke-width=".08"/>`;

  if ($("ver-zonas").checked) {                         // fondo: caja de cada zona
    datos.zonas.forEach((zona, i) => {
      const xs = zona.map((id) => porId[id].x), ys = zona.map((id) => porId[id].y);
      const x0 = Math.min(...xs) - .4, x1 = Math.max(...xs) + .4, y0 = Math.min(...ys) - .4, y1 = Math.max(...ys) + .4;
      svg += `<rect x="${px(x0)}" y="${py(y1)}" width="${x1 - x0}" height="${y1 - y0}" rx=".4" fill="${ZONAS_FONDO[i % ZONAS_FONDO.length]}" opacity=".75"/>`;
    });
  }
  const dep = inst.deposito;
  res.rutas.forEach((ruta, i) => {
    const color = COLORES[i % COLORES.length];
    const puntos = [dep, ...ruta.clientes.map((id) => porId[id]), dep];
    svg += `<polyline points="${puntos.map((p) => px(p.x) + "," + py(p.y)).join(" ")}" fill="none" stroke="${color}" stroke-width=".13" stroke-linejoin="round" opacity=".9"/>`;
  });
  inst.clientes.forEach((c) => {
    const malo = noAtendidos.has(c.id);
    let color = "#adb5bd";
    res.rutas.forEach((r, i) => { if (r.clientes.includes(c.id)) color = COLORES[i % COLORES.length]; });
    svg += `<circle cx="${px(c.x)}" cy="${py(c.y)}" r="${malo ? .26 : .2}" fill="${malo ? "#c62828" : color}" stroke="#fff" stroke-width=".05">`
      + `<title>Cliente ${c.id} · demanda ${c.demanda} · ventana ${c.ventana} · servicio ${c.servicio} min${malo ? " · NO ATENDIDO" : ""}</title></circle>`;
  });
  svg += `<rect x="${dep.x - .4}" y="${py(dep.y) - .4}" width=".8" height=".8" fill="#111" stroke="#fff" stroke-width=".06"><title>Almacén</title></rect>`;
  svg += "</svg>";
  $(idMapa).innerHTML = svg;
}

// ---- detalle de rutas ----------------------------------------------------------------
function dibujarDetalle() {
  const clave = $("sel-estrategia").value, res = datos.resultados[clave];
  let html = "";
  if (!res.rutas.length) html = "<p>Esta estrategia no armó ninguna ruta.</p>";
  res.rutas.forEach((r, i) => {
    html += `<div class="ruta-caja"><h3><span class="punto" style="background:${COLORES[i % COLORES.length]}"></span>`
      + `Vehículo ${r.vehiculo} — ${r.clientes.length} clientes · carga ${r.carga}/${datos.instancia.capacidad} · ${r.km} km · ${r.duracion_h} h</h3>`
      + `<div class="tabla-caja"><table><thead><tr><th>Cliente</th><th>Llega</th><th>Espera (min)</th><th>Empieza</th><th>Ventana</th></tr></thead><tbody>`;
    r.paradas.forEach((p) => {
      html += `<tr><td>${p.id}</td><td>${p.llegada}</td><td>${p.espera_min}</td><td>${p.inicio}</td><td>${p.ventana}</td></tr>`;
    });
    html += "</tbody></table></div></div>";
  });
  if (res.no_atendidos.length) {
    html += `<p class="mal">No atendidos (${res.no_atendidos.length}): ${res.no_atendidos.join(", ")}</p>`;
  }
  if (!res.valida) html += `<p class="mal">⚠ ${res.errores.join("<br>")}</p>`;
  $("detalle-rutas").innerHTML = html;
}

// ---- experimentos -------------------------------------------------------------------
async function cargarGraficos() {
  const caja = $("graficos");
  try {
    const { graficos } = await (await fetch("/api/graficos")).json();
    caja.innerHTML = graficos.length
      ? graficos.map((g) => `<img src="/resultados/${g}" alt="${g}">`).join("")
      : "<p>Todavía no hay gráficos. Ejecuta el benchmark (ver README) y recarga.</p>";
  } catch (e) { caja.textContent = "No se pudieron cargar los gráficos."; }
}

calcular();   // al abrir la página se calcula una instancia de ejemplo
