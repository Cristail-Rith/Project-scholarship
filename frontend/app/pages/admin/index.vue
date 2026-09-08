<template>
    <section class="admin-page">
        <div class="page-heading">
            <div>
                <p class="eyebrow">Restaurant operations</p>
                <h1>Good morning, Administrator</h1>
                <p class="intro">Here is what is happening across FLAVORIA today.</p>
            </div>
            <span class="date-chip">Monday, September 7</span>
        </div>

        <div class="stats-grid">
            <article v-for="stat in stats" :key="stat.label" class="stat-card">
                <span>{{ stat.label }}</span>
                <strong>{{ stat.value }}</strong>
                <small>{{ stat.note }}</small>
            </article>
        </div>

        <div class="dashboard-grid">
            <section class="panel">
                <div class="panel-heading"><div><p class="eyebrow">Live service</p><h2>Recent orders</h2></div><NuxtLink to="/admin/orders">View all &rarr;</NuxtLink></div>
                <div v-for="order in orders" :key="order.id" class="order-row">
                    <span class="order-icon">{{ order.icon }}</span>
                    <span class="order-copy"><strong>{{ order.id }}</strong><small>{{ order.customer }}</small></span>
                    <span class="order-status" :class="order.statusClass">{{ order.status }}</span>
                    <strong class="order-total">{{ order.total }}</strong>
                </div>
            </section>

            <section class="panel availability-panel">
                <div class="panel-heading"><div><p class="eyebrow">Dining room</p><h2>Table availability</h2></div><NuxtLink to="/admin/tables">Manage &rarr;</NuxtLink></div>
                <div class="availability-number"><strong>18</strong><span>of 24 tables available</span></div>
                <div class="availability-track"><span></span></div>
                <div class="availability-meta"><span>6 occupied</span><span>75% available</span></div>
                <p class="panel-note">The evening service is building steadily. Three reservations arrive within the next hour.</p>
            </section>
        </div>
    </section>
</template>

<script setup>
definePageMeta({ layout: 'admin' })

const stats = [
    { label: 'Today\'s revenue', value: '$4,280', note: '+12.8% from yesterday' },
    { label: 'Open orders', value: '24', note: '8 need attention' },
    { label: 'Reservations', value: '36', note: '12 guests arriving soon' },
    { label: 'Menu items', value: '84', note: '4 low-stock ingredients' }
]

const orders = [
    { id: '#FL-2048', customer: 'Sokha Chan · Table 08', status: 'Preparing', statusClass: 'status-preparing', total: '$86.00', icon: '08' },
    { id: '#FL-2047', customer: 'Malis R. · Table 12', status: 'Served', statusClass: 'status-served', total: '$142.50', icon: '12' },
    { id: '#FL-2046', customer: 'Dara K. · Takeaway', status: 'Ready', statusClass: 'status-ready', total: '$54.00', icon: 'TK' }
]
</script>

<style scoped>
.admin-page { color: #29241f; font-family: ui-sans-serif, system-ui, sans-serif; }
.page-heading, .panel-heading, .availability-meta { display: flex; align-items: flex-start; justify-content: space-between; gap: 1rem; }
.eyebrow { margin: 0; color: #b47a2b; font-size: .65rem; font-weight: 700; letter-spacing: .18em; text-transform: uppercase; }
h1, h2 { margin: .45rem 0 0; font-family: Georgia, serif; font-weight: 400; }
h1 { font-size: clamp(2rem, 4vw, 3.5rem); line-height: 1.08; }
h2 { font-size: 1.4rem; }
.intro { margin: .8rem 0 0; color: #8c8176; font-size: .85rem; }
.date-chip { border: 1px solid #e8dfd5; background: #fbf8f3; padding: .7rem .9rem; color: #786e64; font-size: .7rem; }
.stats-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 1rem; margin: 2.5rem 0 1rem; }
.stat-card, .panel { border: 1px solid #e8dfd5; background: #fbf8f3; }
.stat-card { padding: 1.2rem; }
.stat-card span, .stat-card small { display: block; color: #8c8176; font-size: .68rem; }
.stat-card strong { display: block; margin: .8rem 0 .35rem; font-family: Georgia, serif; font-size: 2rem; font-weight: 400; }
.stat-card small { color: #5e9a72; }
.dashboard-grid { display: grid; grid-template-columns: minmax(0, 1.4fr) minmax(18rem, .8fr); gap: 1rem; margin-top: 1rem; }
.panel { padding: 1.4rem; }
.panel-heading { align-items: flex-end; border-bottom: 1px solid #eee6de; padding-bottom: 1rem; }
.panel-heading a { color: #875817; font-size: .7rem; font-weight: 700; text-decoration: none; }
.order-row { display: flex; align-items: center; gap: .8rem; border-bottom: 1px solid #eee6de; padding: 1rem 0; }
.order-row:last-child { border-bottom: 0; padding-bottom: .2rem; }
.order-icon { display: grid; height: 2.2rem; width: 2.2rem; place-items: center; background: #f2e9dc; color: #875817; font-size: .62rem; font-weight: 700; }
.order-copy { flex: 1; min-width: 0; }
.order-copy strong, .order-copy small { display: block; }
.order-copy strong { font-size: .78rem; }
.order-copy small { margin-top: .25rem; color: #8c8176; font-size: .68rem; }
.order-status { padding: .3rem .5rem; font-size: .6rem; font-weight: 700; }
.status-preparing { background: #fff0d9; color: #a46b1e; }.status-served { background: #e5f1e7; color: #4c8059; }.status-ready { background: #e8edf6; color: #526b99; }
.order-total { font-size: .75rem; }
.availability-number { display: flex; align-items: baseline; gap: .7rem; margin-top: 2rem; }.availability-number strong { font-family: Georgia, serif; font-size: 3.5rem; font-weight: 400; }.availability-number span, .availability-meta, .panel-note { color: #8c8176; font-size: .7rem; }
.availability-track { height: .55rem; margin-top: 1.3rem; background: #eee6de; }.availability-track span { display: block; width: 75%; height: 100%; background: #b47a2b; }
.availability-meta { margin-top: .7rem; }.panel-note { margin: 2rem 0 0; line-height: 1.7; }
@media (max-width: 900px) { .stats-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } .dashboard-grid { grid-template-columns: 1fr; } }
@media (max-width: 560px) { .page-heading { flex-direction: column; } .date-chip { align-self: flex-start; } .stats-grid { grid-template-columns: 1fr 1fr; } .order-status { display: none; } }
</style>
    