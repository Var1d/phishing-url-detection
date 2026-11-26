<script setup>
import { computed, onMounted, ref } from "vue"

const url = ref("")
const loading = ref(false)
const error = ref("")
const result = ref(null)
const history = ref([])
const dataset = ref(null)
const evaluation = ref(null)
const importance = ref([])

const resultScore = computed(() =>
  result.value ? `${(result.value.probability * 100).toFixed(2)}%` : ""
)

const signalFeatures = computed(() => {
  if (!result.value) return []
  const preferred = ["is_https", "is_ip", "dom_len", "subdom_cnt", "digit_ratio", "entropy"]
  return preferred
    .filter((key) => result.value.features[key] !== undefined)
    .map((key) => [key, result.value.features[key]])
})

async function fetchJson(path) {
  const response = await fetch(path)
  const data = await response.json()
  if (!response.ok) throw new Error(data.error || "Permintaan gagal.")
  return data
}

async function loadData() {
  try {
    const [datasetData, evaluationData, importanceData] = await Promise.all([
      fetchJson("/api/dataset"),
      fetchJson("/api/evaluation"),
      fetchJson("/api/feature-importance")
    ])
    dataset.value = datasetData
    evaluation.value = evaluationData
    importance.value = importanceData
  } catch (requestError) {
    error.value = requestError.message
  }
}

async function analyzeUrl() {
  error.value = ""
  result.value = null

  if (!url.value.trim()) {
    error.value = "Masukkan URL terlebih dahulu."
    return
  }

  loading.value = true
  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: url.value.trim() })
    })
    const data = await response.json()
    if (!response.ok) throw new Error(data.error || "Prediksi gagal.")

    result.value = data
    history.value.unshift({
      url: url.value.trim(),
      label: data.label,
      score: (data.probability * 100).toFixed(2) + "%"
    })
  } catch (requestError) {
    error.value = requestError.message
  } finally {
    loading.value = false
  }
}

onMounted(loadData)
</script>

<template>
  <main class="min-h-screen overflow-hidden bg-[#101014] text-[#f3f3f5]">
    <div class="pointer-events-none fixed inset-x-0 top-0 h-[470px] opacity-40" aria-hidden="true"
      style="background: repeating-radial-gradient(ellipse at 50% -23%, transparent 0 58px, rgba(255,255,255,.075) 59px 60px, transparent 61px 94px); mask-image: linear-gradient(to bottom, black, transparent);">
    </div>

    <header class="relative z-10 mx-auto flex h-[68px] max-w-[1120px] items-center justify-between px-5">
      <a href="#top" class="flex items-center gap-2 text-[15px] font-medium tracking-tight text-white">
        <span class="grid grid-cols-3 gap-[2px]" aria-hidden="true">
          <i v-for="square in 9" :key="square" class="h-[4px] w-[4px] rounded-[1px] bg-[#7191ff]"></i>
        </span>
        <span>Aegis<span class="text-[#8ba4ff]">Lens</span></span>
      </a>
      <nav class="hidden items-center gap-1 sm:flex" aria-label="Main navigation">
        <a href="#about" class="rounded-md border border-white/[.06] px-3 py-1.5 text-[10px] text-white/65 transition hover:border-white/20 hover:text-white">About</a>
        <a href="#services" class="rounded-md border border-white/[.06] px-3 py-1.5 text-[10px] text-white/65 transition hover:border-white/20 hover:text-white">Services</a>
        <a href="#analysis" class="rounded-md border border-white/[.06] px-3 py-1.5 text-[10px] text-white/65 transition hover:border-white/20 hover:text-white">How it works</a>
        <a href="#evaluation" class="rounded-md border border-white/[.06] px-3 py-1.5 text-[10px] text-white/65 transition hover:border-white/20 hover:text-white">Model</a>
      </nav>
      <a href="#analysis" class="rounded-md border border-white/[.08] px-3 py-1.5 text-[10px] text-white/75 transition hover:border-white/30">Start scan</a>
    </header>

    <section id="top" class="relative z-10 mx-auto px-5 pb-14 pt-10 text-center sm:pb-16 sm:pt-12">
      <div class="mx-auto max-w-[760px]">
        <div class="mb-5 inline-flex items-center gap-2 text-[9px] font-medium uppercase tracking-[.2em] text-white/45">
          <span class="h-1.5 w-1.5 rounded-full bg-[#81d9b8]"></span>
          AI-powered URL security
        </div>
        <h1 class="text-[34px] font-semibold leading-[1.08] tracking-[-1.5px] text-white sm:text-[48px] sm:tracking-[-2px]">
          Add a layer of protection<br class="hidden sm:block" />
          <span>to your </span><span class="rounded-lg bg-[#7895ff] px-2 text-[#111318]">online security</span>
        </h1>
        <p class="mx-auto mt-5 max-w-[570px] text-[11px] leading-[1.8] text-white/50 sm:text-xs">
          Check whether a URL looks benign or phishing before you open it.
          AegisLens examines URL patterns with a machine-learning model — it does not visit the website.
        </p>
        <div class="mt-6 flex justify-center gap-2">
          <a href="#analysis" class="rounded-md bg-[#ffd84d] px-5 py-2.5 text-[10px] font-semibold text-[#181818] transition hover:bg-[#ffe477]">Scan a URL</a>
          <a href="#services" class="rounded-md border border-white/[.12] bg-white/[.04] px-5 py-2.5 text-[10px] text-white/75 transition hover:bg-white/[.08]">How it works</a>
        </div>
        <div v-if="dataset" class="mt-8 flex justify-center gap-8 text-left">
          <div>
            <div class="text-[9px] text-white/40">URLs in dataset</div>
            <div class="mt-1 text-sm font-semibold text-white">{{ dataset.clean_total.toLocaleString() }}</div>
          </div>
          <div class="h-8 w-px bg-white/10"></div>
          <div>
            <div class="text-[9px] text-white/40">URL signals</div>
            <div class="mt-1 text-sm font-semibold text-white">22 features</div>
          </div>
          <div class="h-8 w-px bg-white/10"></div>
          <div>
            <div class="text-[9px] text-white/40">Model</div>
            <div class="mt-1 text-sm font-semibold text-white">Random Forest</div>
          </div>
        </div>
      </div>
    </section>

    <section id="about" class="relative z-10 mx-auto max-w-[900px] px-5 pb-16">
      <div class="rounded-xl border border-white/[.07] bg-gradient-to-b from-white/[.045] to-white/[.015] px-6 py-8 sm:px-10">
        <div class="text-center">
          <h2 class="text-sm font-semibold text-white">What AegisLens does</h2>
          <p class="mt-1 text-[9px] text-white/45">A quick, transparent check before you visit a link.</p>
        </div>
        <div class="mt-7 grid gap-5 sm:grid-cols-3 sm:gap-6">
          <div class="flex items-start gap-3">
            <span class="grid h-8 w-8 shrink-0 place-items-center rounded-full border border-white/[.08] bg-white/[.04] text-[#a3afff]">
              <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="10.8" cy="10.8" r="6.8"/><path d="m16 16 4.5 4.5M8 11h5M10.5 8.5v5"/></svg>
            </span>
            <div><h3 class="text-[10px] font-medium text-white/85">URL pattern analysis</h3><p class="mt-1 text-[9px] leading-4 text-white/45">Checks domain, protocol and character patterns.</p></div>
          </div>
          <div class="flex items-start gap-3">
            <span class="grid h-8 w-8 shrink-0 place-items-center rounded-full border border-white/[.08] bg-white/[.04] text-[#a3afff]">
              <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 3 5 6v5c0 4.8 2.9 8.2 7 10 4.1-1.8 7-5.2 7-10V6l-7-3Z"/><path d="m9 12 2 2 4-5"/></svg>
            </span>
            <div><h3 class="text-[10px] font-medium text-white/85">Model-based screening</h3><p class="mt-1 text-[9px] leading-4 text-white/45">Classifies URLs as benign or potentially phishing.</p></div>
          </div>
          <div class="flex items-start gap-3">
            <span class="grid h-8 w-8 shrink-0 place-items-center rounded-full border border-white/[.08] bg-white/[.04] text-[#a3afff]">
              <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="4" y="4" width="16" height="16" rx="3"/><path d="M8 9h8M8 12h5M8 15h7"/></svg>
            </span>
            <div><h3 class="text-[10px] font-medium text-white/85">Clear explanations</h3><p class="mt-1 text-[9px] leading-4 text-white/45">See the model score and selected URL signals.</p></div>
          </div>
        </div>
      </div>
    </section>

    <section id="services" class="relative z-10 mx-auto max-w-[900px] px-5 pb-16">
      <div class="mx-auto mb-7 max-w-[470px] text-center">
        <div class="text-[9px] font-medium uppercase tracking-[.2em] text-[#91a5ff]">Simple. Focused. Transparent.</div>
        <h2 class="mt-2 text-[23px] font-semibold leading-tight tracking-[-.6px] text-white sm:text-[27px]">A smarter first step against<br class="hidden sm:block" /> suspicious links.</h2>
        <p class="mt-3 text-[10px] leading-5 text-white/45">Understand the URL, review the prediction, and make an informed decision.</p>
      </div>
      <div class="grid overflow-hidden rounded-xl border border-white/[.08] sm:grid-cols-3">
        <article class="border-b border-white/[.08] bg-white/[.025] p-5 sm:border-b-0 sm:border-r">
          <span class="grid h-8 w-8 place-items-center rounded-full bg-white/[.06] text-[#a3afff]">
            <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.5 3.5 5.5 3.5 9S14.5 18.5 12 21c-2.5-2.5-3.5-5.5-3.5-9S9.5 5.5 12 3Z"/></svg>
          </span>
          <h3 class="mt-4 text-[11px] font-semibold text-white">Inspect URL signals</h3>
          <p class="mt-2 min-h-10 text-[9px] leading-4 text-white/45">Review characteristics like domain structure, HTTPS, digits and URL complexity.</p>
          <a href="#analysis" class="mt-4 inline-flex items-center gap-2 rounded border border-white/[.08] px-3 py-1.5 text-[9px] text-white/75 hover:border-white/20">Explore analysis <span aria-hidden="true">→</span></a>
        </article>
        <article class="border-b border-white/[.08] bg-white/[.045] p-5 sm:border-b-0 sm:border-r">
          <span class="grid h-8 w-8 place-items-center rounded-full bg-white/[.06] text-[#a3afff]">
            <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M12 3 5 6v5c0 4.8 2.9 8.2 7 10 4.1-1.8 7-5.2 7-10V6l-7-3Z"/><path d="M12 8v4m0 4h.01"/></svg>
          </span>
          <h3 class="mt-4 text-[11px] font-semibold text-white">Get a risk prediction</h3>
          <p class="mt-2 min-h-10 text-[9px] leading-4 text-white/45">See whether the model classifies a URL as benign or potentially phishing.</p>
          <a href="#analysis" class="mt-4 inline-flex items-center gap-2 rounded border border-white/[.08] px-3 py-1.5 text-[9px] text-white/75 hover:border-white/20">Start a scan <span aria-hidden="true">→</span></a>
        </article>
        <article class="bg-white/[.025] p-5">
          <span class="grid h-8 w-8 place-items-center rounded-full bg-white/[.06] text-[#a3afff]">
            <svg viewBox="0 0 24 24" class="h-4 w-4" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M4 19V5m0 14h16M8 15l3-4 3 2 5-7"/></svg>
          </span>
          <h3 class="mt-4 text-[11px] font-semibold text-white">Review model insights</h3>
          <p class="mt-2 min-h-10 text-[9px] leading-4 text-white/45">Explore evaluation metrics and the features that influence the model.</p>
          <a href="#evaluation" class="mt-4 inline-flex items-center gap-2 rounded border border-white/[.08] px-3 py-1.5 text-[9px] text-white/75 hover:border-white/20">View model <span aria-hidden="true">→</span></a>
        </article>
      </div>
    </section>

    <section id="analysis" class="relative z-10 mx-auto max-w-[900px] scroll-mt-6 px-5 pb-16">
      <div class="rounded-xl border border-white/[.08] bg-gradient-to-b from-white/[.045] to-white/[.015] p-5 sm:p-8">
        <div class="mx-auto max-w-[610px] text-center">
          <div class="text-[9px] font-medium uppercase tracking-[.2em] text-[#91a5ff]">URL checker</div>
          <h2 class="mt-2 text-xl font-semibold text-white">Check a link before you open it</h2>
          <p class="mt-2 text-[10px] leading-5 text-white/45">Paste the complete URL below. We analyze its structure only; we never open the link.</p>
          <form class="mt-5 flex flex-col gap-2 sm:flex-row" @submit.prevent="analyzeUrl">
            <input v-model="url" type="text" placeholder="https://example.com/login"
              aria-label="URL yang akan dianalisis"
              class="h-11 min-w-0 flex-1 rounded-md border border-white/[.1] bg-[#0c0c10] px-3 text-xs text-white outline-none placeholder:text-white/25 focus:border-[#7895ff]/70" />
            <button type="submit" :disabled="loading"
              class="h-11 rounded-md bg-[#ffd84d] px-5 text-[10px] font-semibold text-[#181818] transition hover:bg-[#ffe477] disabled:cursor-wait disabled:opacity-60">
              {{ loading ? "Analyzing..." : "Analyze URL" }}
            </button>
          </form>
          <div v-if="error" role="alert" class="mt-3 rounded-md border border-rose-400/20 bg-rose-400/[.08] px-4 py-3 text-left text-[10px] text-rose-200">{{ error }}</div>
        </div>

        <div v-if="result" class="mx-auto mt-5 max-w-[610px] overflow-hidden rounded-lg border"
          :class="result.label === 'Phishing' ? 'border-rose-400/25' : 'border-emerald-300/25'">
          <div class="flex items-center justify-between px-4 py-3"
            :class="result.label === 'Phishing' ? 'bg-rose-400/[.08]' : 'bg-emerald-300/[.07]'">
            <div>
              <div class="text-[9px] uppercase tracking-wider text-white/45">Model prediction</div>
              <div class="mt-1 flex items-center gap-2 text-sm font-semibold text-white">
                <span class="h-2 w-2 rounded-full" :class="result.label === 'Phishing' ? 'bg-rose-400' : 'bg-emerald-300'"></span>
                {{ result.label === 'Phishing' ? 'Potentially phishing' : 'Classified as benign' }}
              </div>
            </div>
            <div class="text-right">
              <div class="text-base font-semibold text-white">{{ resultScore }}</div>
              <div class="text-[9px] text-white/40">predicted class score</div>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-px border-t border-white/[.07] bg-white/[.07] sm:grid-cols-3">
            <div v-for="[key, value] in signalFeatures" :key="key" class="bg-[#141418] px-3 py-2.5">
              <div class="truncate text-[8px] uppercase tracking-wider text-white/40">{{ key.replaceAll('_', ' ') }}</div>
              <div class="mt-1 text-xs font-medium text-white/80">{{ typeof value === 'number' && value < 1 ? value.toFixed(4) : value }}</div>
            </div>
          </div>
          <div class="border-t border-white/[.07] px-4 py-3 text-[9px] leading-4 text-white/40">
            This is a machine-learning prediction based on URL patterns. It does not confirm whether the website is safe, active, or owned by a particular organization.
          </div>
        </div>
      </div>
    </section>

    <section v-if="dataset" class="relative z-10 mx-auto max-w-[900px] px-5 pb-14">
      <div class="mb-4 text-center">
        <div class="text-[9px] font-medium uppercase tracking-[.2em] text-[#91a5ff]">Project data</div>
        <h2 class="mt-2 text-lg font-semibold text-white">The model behind the scan</h2>
      </div>
      <div class="grid grid-cols-2 gap-px overflow-hidden rounded-lg border border-white/[.07] bg-white/[.07] sm:grid-cols-4">
        <div v-for="item in [
          ['Dataset rows', dataset.clean_total],
          ['Benign URLs', dataset.benign],
          ['Phishing URLs', dataset.phishing],
          ['Test samples', evaluation?.test_total ?? '—']
        ]" :key="item[0]" class="bg-[#141418] p-4 text-center">
          <div class="text-[8px] uppercase tracking-wider text-white/40">{{ item[0] }}</div>
          <div class="mt-2 text-lg font-semibold text-white">{{ typeof item[1] === 'number' ? item[1].toLocaleString() : item[1] }}</div>
        </div>
      </div>
    </section>

    <section v-if="evaluation" id="evaluation" class="relative z-10 mx-auto max-w-[900px] scroll-mt-6 px-5 pb-16">
      <div class="mb-5 text-center">
        <div class="text-[9px] font-medium uppercase tracking-[.2em] text-[#91a5ff]">Model performance</div>
        <h2 class="mt-2 text-lg font-semibold text-white">Evaluation metrics</h2>
        <p class="mt-1 text-[9px] text-white/40">Measured on a held-out test set; results do not guarantee future predictions.</p>
      </div>
      <div class="grid grid-cols-2 gap-px overflow-hidden rounded-lg border border-white/[.07] bg-white/[.07] sm:grid-cols-4">
        <article v-for="item in [
          ['Accuracy', evaluation.accuracy],
          ['Precision', evaluation.precision],
          ['Recall', evaluation.recall],
          ['F1-score', evaluation.f1]
        ]" :key="item[0]" class="bg-[#141418] p-4 text-center">
          <div class="text-[9px] text-white/45">{{ item[0] }}</div>
          <div class="mt-2 text-xl font-semibold text-white">{{ (item[1] * 100).toFixed(2) }}%</div>
        </article>
      </div>
      <div class="mt-3 grid gap-3 md:grid-cols-2">
        <article class="rounded-lg border border-white/[.07] bg-white/[.025] p-4">
          <h3 class="mb-3 text-[10px] font-semibold text-white">Confusion matrix</h3>
          <div class="grid grid-cols-[82px_1fr_1fr] gap-1.5 text-center">
            <div></div><div class="grid place-items-center text-[8px] text-white/40">Pred. benign</div><div class="grid place-items-center text-[8px] text-white/40">Pred. phishing</div>
            <div class="grid place-items-center text-[8px] text-white/40">Actual benign</div>
            <div class="grid min-h-12 place-items-center rounded bg-emerald-300/[.07] text-sm text-emerald-200">{{ evaluation.tn }}</div>
            <div class="grid min-h-12 place-items-center rounded bg-rose-400/[.07] text-sm text-rose-200">{{ evaluation.fp }}</div>
            <div class="grid place-items-center text-[8px] text-white/40">Actual phishing</div>
            <div class="grid min-h-12 place-items-center rounded bg-rose-400/[.07] text-sm text-rose-200">{{ evaluation.fn }}</div>
            <div class="grid min-h-12 place-items-center rounded bg-emerald-300/[.07] text-sm text-emerald-200">{{ evaluation.tp }}</div>
          </div>
        </article>
        <article class="rounded-lg border border-white/[.07] bg-white/[.025] p-4">
          <h3 class="mb-3 text-[10px] font-semibold text-white">Most influential URL features</h3>
          <div v-for="item in importance.slice(0, 5)" :key="item.feature" class="mb-2.5">
            <div class="mb-1 flex justify-between text-[9px] text-white/55"><span>{{ item.feature }}</span><span>{{ (item.importance * 100).toFixed(2) }}%</span></div>
            <div class="h-1 overflow-hidden rounded-full bg-white/[.07]"><div class="h-full rounded-full bg-[#829bff]" :style="{ width: `${Math.min(item.importance * 100 * 3, 100)}%` }"></div></div>
          </div>
        </article>
      </div>
    </section>

    <section v-if="history.length" id="history" class="relative z-10 mx-auto max-w-[900px] px-5 pb-14">
      <div class="mb-4 flex items-end justify-between">
        <div><div class="text-[9px] font-medium uppercase tracking-[.2em] text-[#91a5ff]">Recent scans</div><h2 class="mt-1 text-base font-semibold text-white">Analysis history</h2></div>
        <button class="text-[9px] text-white/50 hover:text-white" @click="history = []">Clear history</button>
      </div>
      <div class="overflow-hidden rounded-lg border border-white/[.07]">
        <div class="grid grid-cols-[minmax(0,1fr)_110px_65px] gap-3 bg-white/[.04] px-3 py-2 text-[8px] uppercase tracking-wider text-white/40"><span>URL</span><span>Result</span><span>Score</span></div>
        <div v-for="item in history" :key="item.url" class="grid grid-cols-[minmax(0,1fr)_110px_65px] items-center gap-3 border-t border-white/[.06] px-3 py-3 text-[10px]">
          <span class="truncate text-white/70">{{ item.url }}</span>
          <span :class="item.label === 'Phishing' ? 'text-rose-300' : 'text-emerald-200'">{{ item.label }}</span>
          <span class="text-white/60">{{ item.score }}</span>
        </div>
      </div>
    </section>

    <footer class="relative z-10 mx-auto flex max-w-[900px] items-center justify-between border-t border-white/[.07] px-5 py-6 text-[8px] uppercase tracking-wider text-white/35">
      <span>AegisLens · URL risk analysis</span>
      <span>AI-assisted, not a security guarantee</span>
    </footer>
  </main>
</template>
