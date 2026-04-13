import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet,
  Alert, Modal, Dimensions, Platform, StatusBar, Vibration,
  AppState, Switch
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

// ─── COLORES ────────────────────────────────────────────────────────────────
const C = {
  bg: '#0B0E12', card: '#141920', card2: '#1A1F28', border: '#232B36',
  faint: '#1E252F', teal: '#17C4A0', tealBg: '#0A2018', tealBorder: '#124830',
  red: '#E05555', redBg: '#221010', redBorder: '#4A1818',
  amber: '#E8A838', amberBg: '#221A08', amberBorder: '#4A3010',
  green: '#4DBD8F', greenBg: '#0A1E14', greenBorder: '#124830',
  blue: '#4A9EE8', blueBg: '#0A1420',
  purple: '#9B7FE8', purpleBg: '#150D2A',
  text: '#DDE2DC', muted: '#5A6472',
};

// ─── CONSTANTES ─────────────────────────────────────────────────────────────
const LEVELS = [
  { min: 0,  label: 'Novato',      icon: '🌱', color: C.red },
  { min: 25, label: 'Despertando', icon: '👁',  color: C.amber },
  { min: 50, label: 'Controlado',  icon: '💪', color: C.teal },
  { min: 75, label: 'Espartano',   icon: '⚔️', color: C.green },
  { min: 95, label: 'Maestro Zen', icon: '🏆', color: '#FFD700' },
];
const CATS = ['Tecnología','Entretenimiento','Ropa','Hogar','Trabajo','Vehículo','Salud','Comida','Otro'];
const REMINDER_OPTIONS = [2, 4, 6, 8, 10, 12];

// ─── UTILS ──────────────────────────────────────────────────────────────────
const fmt = n => '$' + Math.round(n).toLocaleString('es-CL');
const fmtS = n => n >= 1e6 ? `$${(n/1e6).toFixed(1)}M` : n >= 1000 ? `$${Math.round(n/1000)}K` : fmt(n);
const uid = () => Math.random().toString(36).slice(2, 9);
const toDays = (n, s) => s > 0 ? (n / (s / 30)).toFixed(1) : '0';
const toHrs = (n, s) => s > 0 ? Math.round(n / (s / 30 / 8)) : 0;
const isNight = () => { const h = new Date().getHours(); return h >= 22 || h < 6; };
const isWE = () => [0, 6].includes(new Date().getDay());

const getHourMessage = (nombre, libre, sm, score) => {
  const h = new Date().getHours();
  const dias = toDays(libre, sm);
  if (h >= 6 && h < 12) return `☀️ Buenos días, ${nombre}. Tienes ${fmt(libre)} libres hoy. Úsalos con propósito.`;
  if (h >= 12 && h < 15) return `🌤 Mediodía. Tu meta financiera te está esperando. Tienes ${fmt(libre)} disponibles.`;
  if (h >= 15 && h < 20) return `🌆 Tarde peligrosa. Antes de comprar algo, consulta la app. Libre: ${fmt(libre)}.`;
  if (h >= 20 && h < 22) return `🌙 Noche. Hora de compras online impulsivas. Cuidado. Saldo libre: ${fmt(libre)}.`;
  return `🌛 Son las ${h}h. Tu horario de mayor riesgo. No compres nada ahora. Libre: ${fmt(libre)}.`;
};

// ─── ANÁLISIS LOCAL ──────────────────────────────────────────────────────────
function analizarLocal(nombre, val, motivo, libre, sm, similares, metas, relapseMode) {
  const dias = toDays(val, sm);
  const pct = libre > 0 ? val / libre : 1;
  const tieneSimilar = similares.length > 0;
  const motivoVago = !motivo || motivo.length < 8 || /quiero|porque sí|no sé|ganas/i.test(motivo);
  const metaAfectada = metas.find(m => !m.completada);

  let v = 'verde';
  if (pct > 0.7 || relapseMode) v = 'rojo';
  else if (pct > 0.35 || tieneSimilar || motivoVago || isNight() || isWE()) v = 'amarillo';

  const msgs = {
    rojo: `❌ ROJO — No lo hagas ahora, ${nombre}\n\nEsto consume más del 70% de tu dinero libre. No es el momento.\n\nEquivale a ${dias} días de trabajo. Solo quedarían ${fmt(libre - val)}.\n\n💡 Agrégalo a la lista de espera. Tu yo del futuro te lo agradecerá.`,
    amarillo: tieneSimilar
      ? `⚠️ AMARILLO — Ya tienes algo similar\n\nTienes "${similares[0].nombre}" que cumple una función parecida. ¿Realmente necesitas otro?\n\nEquivale a ${dias} días de trabajo. Te quedarían ${fmt(libre - val)}.\n\n💡 Usa lo que tienes 30 días más. Si sigue siendo insuficiente, ahí decides.`
      : motivoVago
      ? `⚠️ AMARILLO — El motivo no convence\n\n"Simplemente lo quiero" no justifica gastar ${fmt(val)}. Eso es un impulso puro.\n\nEquivale a ${dias} días de trabajo. Te quedarían ${fmt(libre - val)}.\n\n💡 Escribe en papel por qué lo necesitas. Si no puedes convencerte, no lo compres.`
      : `⚠️ AMARILLO — Piénsalo bien\n\nNo es imposible, pero ${fmt(val)} merece una pausa.\n\nEquivale a ${dias} días de trabajo. Te quedarían ${fmt(libre - val)}.\n\n💡 Espera 48 horas. Las compras que resisten la espera, valen la pena.`,
    verde: `✅ VERDE — Parece razonable\n\nEstá dentro de tu margen y ${motivo.length > 5 ? 'tienes una razón clara' : 'no compromete tu estabilidad'}.\n\nEquivale a ${dias} días de trabajo. Te quedarían ${fmt(libre - val)}.\n\n💡 Si lo necesitas de verdad, adelante. Si tienes dudas, espera un día.`,
  };

  let texto = msgs[v];
  if (metaAfectada && v !== 'verde') {
    const dL = Math.ceil(val / (sm / 30));
    texto += `\n\n🎯 Esto retrasa tu meta "${metaAfectada.nombre}" ~${dL} días.`;
  }
  return { texto, v };
}

// ─── STORAGE ────────────────────────────────────────────────────────────────
const save = async (k, v) => { try { await AsyncStorage.setItem(k, JSON.stringify(v)); } catch {} };
const load = async k => { try { const v = await AsyncStorage.getItem(k); return v ? JSON.parse(v) : null; } catch { return null; } };

// ═══════════════════════════════════════════════════════════════════════════
// COMPONENTES BASE
// ═══════════════════════════════════════════════════════════════════════════
const GCard = ({ children, style, accent }) => (
  <View style={[styles.card, accent ? { borderColor: accent } : {}, style]}>{children}</View>
);

const GBtn = ({ onPress, label, variant = 'primary', disabled, full, style }) => {
  const variants = {
    primary: { bg: C.teal, text: C.bg, border: C.teal },
    ghost: { bg: 'transparent', text: C.muted, border: C.border },
    danger: { bg: C.redBg, text: C.red, border: C.redBorder },
    amber: { bg: C.amberBg, text: C.amber, border: C.amberBorder },
    green: { bg: C.greenBg, text: C.green, border: C.greenBorder },
    purple: { bg: C.purpleBg, text: C.purple, border: '#3A2070' },
  };
  const v = variants[variant] || variants.primary;
  return (
    <TouchableOpacity onPress={onPress} disabled={disabled} activeOpacity={0.7}
      style={[styles.btn, { backgroundColor: v.bg, borderColor: v.border, opacity: disabled ? 0.4 : 1, width: full ? '100%' : 'auto' }, style]}>
      <Text style={[styles.btnText, { color: v.text }]}>{label}</Text>
    </TouchableOpacity>
  );
};

const GInp = ({ placeholder, value, onChangeText, secureTextEntry, keyboardType, style }) => (
  <TextInput
    placeholder={placeholder} value={value} onChangeText={onChangeText}
    secureTextEntry={secureTextEntry} keyboardType={keyboardType || 'default'}
    placeholderTextColor={C.muted}
    style={[styles.input, style]}/>
);

const MBar = ({ pct, color, height = 6 }) => (
  <View style={[styles.barBg, { height }]}>
    <View style={[styles.barFill, { width: `${Math.min(100, Math.max(0, pct))}%`, backgroundColor: color || C.teal, height }]}/>
  </View>
);

const Row = ({ label, value, color, bold }) => (
  <View style={styles.row}>
    <Text style={styles.rowLabel}>{label}</Text>
    <Text style={[styles.rowValue, color ? { color } : {}, bold ? { fontWeight: '700' } : {}]}>{value}</Text>
  </View>
);

// ═══════════════════════════════════════════════════════════════════════════
// PANTALLA BIENVENIDA
// ═══════════════════════════════════════════════════════════════════════════
function Bienvenida({ onStart }) {
  const [nombre, setNombre] = useState('');
  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.center}>
      <StatusBar barStyle="light-content" backgroundColor={C.bg}/>
      <View style={styles.logoBox}>
        <Text style={styles.logoEmoji}>🛑</Text>
        <Text style={styles.logoTitle}>GASTO CERO</Text>
        <Text style={styles.logoSub}>La app que te frena antes de gastar de más</Text>
      </View>
      {[
        ['🛑', 'Frena los impulsos antes de comprar'],
        ['🎯', 'Conecta tus gastos con tus metas'],
        ['⏰', 'Recordatorios inteligentes cada X horas'],
        ['🔐', 'Saldo oculto con PIN personal'],
        ['💸', '100% gratis · Sin internet'],
      ].map(([icon, text], i) => (
        <View key={i} style={styles.featureRow}>
          <Text style={styles.featureIcon}>{icon}</Text>
          <Text style={styles.featureText}>{text}</Text>
        </View>
      ))}
      <GCard style={{ width: '100%', marginTop: 20 }}>
        <Text style={styles.label}>¿Cómo te llamas?</Text>
        <GInp placeholder="Tu nombre" value={nombre} onChangeText={setNombre}/>
        <GBtn label="Entrar gratis →" onPress={() => nombre.trim() && onStart(nombre.trim())}
          disabled={!nombre.trim()} full style={{ marginTop: 14 }}/>
      </GCard>
      <Text style={styles.disclaimer}>Sin correo · Sin contraseña · Sin publicidad</Text>
    </ScrollView>
  );
}

// ═══════════════════════════════════════════════════════════════════════════
// SETUP SUELDO
// ═══════════════════════════════════════════════════════════════════════════
function Setup({ nombre, onDone }) {
  const [sueldo, setSueldo] = useState('');
  const [frec, setFrec] = useState('mensual');
  const sm = frec === 'quincenal' ? parseFloat(sueldo.replace(/\D/g, '')) * 2
           : frec === 'semanal' ? parseFloat(sueldo.replace(/\D/g, '')) * 4
           : parseFloat(sueldo.replace(/\D/g, '')) || 0;
  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.center}>
      <Text style={styles.logoTitle}>💰 ¿Cuánto ganas?</Text>
      <Text style={styles.logoSub}>Lo que te depositan, no el bruto</Text>
      <GCard style={{ width: '100%', marginTop: 20 }}>
        <Text style={styles.label}>Frecuencia de pago</Text>
        <View style={styles.frecRow}>
          {['mensual', 'quincenal', 'semanal'].map(f => (
            <TouchableOpacity key={f} onPress={() => setFrec(f)} style={[styles.frecBtn, frec === f && styles.frecBtnActive]}>
              <Text style={[styles.frecText, frec === f && styles.frecTextActive]}>{f}</Text>
            </TouchableOpacity>
          ))}
        </View>
        <Text style={styles.label}>Monto líquido</Text>
        <GInp placeholder="Ej: 2300000" value={sueldo} onChangeText={setSueldo} keyboardType="numeric"/>
        {sm > 0 && (
          <View style={[styles.infoBg, { marginTop: 12 }]}>
            <Text style={styles.infoLabel}>Mensual equivalente</Text>
            <Text style={styles.infoValue}>{fmt(sm)}</Text>
            <Text style={styles.infoSub}>{fmt(sm / 30)}/día · {fmt(sm / 30 / 8)}/hora</Text>
          </View>
        )}
        <GBtn label="¡Empezar! →" onPress={() => sm > 0 && onDone({ nombre, sueldoMensual: sm, profileType: 'racional', score: 50, accounts: [], debts: [], items: [], wishlist: [], history: [], purchases: [], metas: [], pin: null, reminderHours: 8, priorities: { basico: Math.round(sm * .35), seguridad: Math.round(sm * .30), crecimiento: Math.round(sm * .15), gustos: Math.round(sm * .20) } })}
          disabled={!sm} full style={{ marginTop: 14 }}/>
      </GCard>
    </ScrollView>
  );
}

// ═══════════════════════════════════════════════════════════════════════════
// PANTALLA PIN
// ═══════════════════════════════════════════════════════════════════════════
function PinScreen({ title, onSuccess, onCancel, creating }) {
  const [pin, setPin] = useState('');
  const [confirm, setConfirm] = useState('');
  const [step, setStep] = useState(creating ? 'create' : 'enter');

  const handleDigit = (d) => {
    if (step === 'create') {
      const next = (pin + d).slice(0, 4);
      setPin(next);
      if (next.length === 4) setStep('confirm');
    } else if (step === 'confirm') {
      const next = (confirm + d).slice(0, 4);
      setConfirm(next);
      if (next.length === 4) {
        if (next === pin) { onSuccess(pin); }
        else { Alert.alert('Error', 'Los PINs no coinciden'); setPin(''); setConfirm(''); setStep('create'); }
      }
    } else {
      const next = (pin + d).slice(0, 4);
      setPin(next);
      if (next.length === 4) onSuccess(next);
    }
  };

  const current = step === 'confirm' ? confirm : pin;
  const subtitle = step === 'create' ? 'Crea tu PIN de 4 dígitos' : step === 'confirm' ? 'Confirma tu PIN' : title;

  return (
    <View style={[styles.screen, styles.center, { backgroundColor: C.bg }]}>
      <Text style={styles.pinTitle}>🔐 {subtitle}</Text>
      <View style={styles.pinDots}>
        {[0,1,2,3].map(i => <View key={i} style={[styles.pinDot, current.length > i && styles.pinDotFilled]}/>)}
      </View>
      <View style={styles.pinGrid}>
        {['1','2','3','4','5','6','7','8','9','','0','⌫'].map((d, i) => (
          <TouchableOpacity key={i} style={[styles.pinKey, !d && styles.pinKeyEmpty]}
            onPress={() => { if (d === '⌫') { if (step === 'confirm') setConfirm(c => c.slice(0,-1)); else setPin(p => p.slice(0,-1)); } else if (d) handleDigit(d); }}>
            {d ? <Text style={styles.pinKeyText}>{d}</Text> : null}
          </TouchableOpacity>
        ))}
      </View>
      {onCancel && <GBtn label="Cancelar" variant="ghost" onPress={onCancel} style={{ marginTop: 16 }}/>}
    </View>
  );
}

// ═══════════════════════════════════════════════════════════════════════════
// PANTALLA SALDO OCULTO
// ═══════════════════════════════════════════════════════════════════════════
function SaldoOculto({ libre, sm, nombre, pin, onSetPin, onClose }) {
  const [revealed, setRevealed] = useState(false);
  const [showPin, setShowPin] = useState(false);

  const revelar = () => {
    if (!pin) { Alert.alert('Sin PIN', 'Configura un PIN primero en Ajustes'); return; }
    setShowPin(true);
  };

  if (showPin && !revealed) {
    return <PinScreen title="Ingresa tu PIN para ver el saldo" onSuccess={p => { if (p === pin) { setRevealed(true); setShowPin(false); Vibration.vibrate(100); } else { Alert.alert('PIN incorrecto', 'Intenta de nuevo'); setShowPin(false); } }} onCancel={() => setShowPin(false)}/>;
  }

  const h = new Date().getHours();
  const riesgo = isNight() || isWE();

  return (
    <ScrollView style={styles.screen} contentContainerStyle={{ padding: 20, paddingBottom: 40 }}>
      <View style={styles.saldoHeader}>
        <Text style={styles.saldoNombre}>{nombre}</Text>
        <TouchableOpacity onPress={onClose}><Text style={{ color: C.muted, fontSize: 22 }}>×</Text></TouchableOpacity>
      </View>

      <GCard style={{ alignItems: 'center', marginBottom: 16 }}>
        <Text style={styles.saldoLabel}>Tu dinero libre este mes</Text>
        {revealed ? (
          <>
            <Text style={[styles.saldoMonto, { color: libre > sm * .5 ? C.green : libre > sm * .25 ? C.amber : C.red }]}>{fmt(libre)}</Text>
            <Text style={styles.saldoDias}>{toDays(libre, sm)} días de trabajo disponibles</Text>
            <GBtn label="Ocultar saldo" variant="ghost" onPress={() => setRevealed(false)} style={{ marginTop: 10 }}/>
          </>
        ) : (
          <>
            <Text style={styles.saldoOculto}>$ • • • • •</Text>
            <GBtn label="Ver saldo (PIN)" variant="primary" onPress={revelar} style={{ marginTop: 10 }}/>
          </>
        )}
      </GCard>

      {riesgo && (
        <GCard accent={C.amberBorder} style={{ backgroundColor: C.amberBg, marginBottom: 12 }}>
          <Text style={[styles.alertText, { color: C.amber }]}>
            {isNight() ? `🌙 Son las ${h}h. Horario de riesgo. Evita compras ahora.` : '📅 Fin de semana: compramos un 40% más. Cuidado.'}
          </Text>
        </GCard>
      )}

      <GCard style={{ backgroundColor: C.tealBg, borderColor: C.tealBorder }}>
        <Text style={[styles.sectionTitle, { color: C.teal }]}>Costo real en tiempo</Text>
        {[[5000,'Comida del día'],[20000,'Cena para dos'],[50000,'Fin de semana'],[100000,'Fin de semana largo']].map(([v,l],i) => (
          <Row key={i} label={`${l} (${fmt(v)})`} value={`${toHrs(v, sm)}h trabajo`} color={C.amber}/>
        ))}
      </GCard>

      <GBtn label="⚡ ¿Necesito comprar algo?" variant="primary" full onPress={onClose} style={{ marginTop: 8 }}/>
    </ScrollView>
  );
}

// ═══════════════════════════════════════════════════════════════════════════
// MAIN APP
// ═══════════════════════════════════════════════════════════════════════════
export default function App() {
  const [perfil, setPerfil] = useState(null);
  const [nombre, setNombre] = useState(null);
  const [ready, setReady] = useState(false);
  const [tab, setTab] = useState('dashboard');
  const [showSaldo, setShowSaldo] = useState(false);
  const [showSetPin, setShowSetPin] = useState(false);

  // Purchase flow
  const [pur, setPur] = useState({ nombre: '', valor: '', motivo: '' });
  const [purStep, setPurStep] = useState(0);
  const [countdown, setCountdown] = useState(10);
  const [analisis, setAnalisis] = useState(null);
  const timerRef = useRef(null);

  // Forms
  const [newDebt, setNewDebt] = useState({ nombre: '', cuota: '' });
  const [newItem, setNewItem] = useState({ nombre: '', cat: 'Tecnología', cantidad: '1', uso: 'semanal', valor: '' });
  const [newMeta, setNewMeta] = useState({ nombre: '', montoObj: '', montoActual: '' });
  const [showForms, setShowForms] = useState({ debt: false, item: false, meta: false });
  const [editSueldo, setEditSueldo] = useState('');
  const [editingS, setEditingS] = useState(false);
  const [shareCode, setShareCode] = useState('');
  const [simExtra, setSimExtra] = useState(0);

  useEffect(() => {
    Promise.all([load('gc_perfil'), load('gc_nombre')]).then(([p, n]) => {
      setPerfil(p); setNombre(n); setReady(true);
    });
  }, []);

  // Friction countdown
  useEffect(() => {
    if (purStep === 1) {
      setCountdown(10);
      timerRef.current = setInterval(() => {
        setCountdown(c => { if (c <= 1) { clearInterval(timerRef.current); setPurStep(2); return 0; } return c - 1; });
      }, 1000);
    }
    return () => clearInterval(timerRef.current);
  }, [purStep]);

  const up = useCallback(next => { setPerfil(next); save('gc_perfil', next); }, []);
  const addScore = (delta, reason) => {
    setPerfil(prev => {
      const next = { ...prev, score: Math.max(0, Math.min(100, (prev.score || 50) + delta)), history: [{ id: uid(), reason, delta, ts: new Date().toLocaleString('es-CL', { hour: '2-digit', minute: '2-digit', day: '2-digit', month: '2-digit' }) }, ...(prev.history || [])].slice(0, 60) };
      save('gc_perfil', next); return next;
    });
  };

  if (!ready) return <View style={[styles.screen, styles.center]}><Text style={{ color: C.muted }}>Cargando...</Text></View>;
  if (!nombre) return <Bienvenida onStart={n => { save('gc_nombre', n); setNombre(n); }}/>;
  if (!perfil) return <Setup nombre={nombre} onDone={data => up(data)}/>;

  const { sueldoMensual: sm = 0, accounts = [], debts = [], items = [], wishlist = [], history = [], score = 50, metas = [], purchases = [], pin, reminderHours = 8 } = perfil;
  const totalD = debts.reduce((s, d) => s + d.cuota, 0);
  const totalSaldo = accounts.reduce((s, a) => s + a.balance, 0);
  const libre = sm - totalD;
  const presion = sm > 0 ? Math.round((totalD / sm) * 100) : 0;
  const level = [...LEVELS].reverse().find(l => score >= l.min) || LEVELS[0];
  const badStreak = history.filter(h => h.delta < 0).slice(0, 5).length;
  const relapseMode = badStreak >= 3;
  const activeMetas = (metas || []).filter(m => !m.completada);
  const savedDec = history.filter(h => h.delta > 0 && h.reason.includes('Evitó'));

  const hacerAnalisis = () => {
    const val = parseInt(pur.valor.replace(/\D/g, '')) || 0;
    const similares = items.filter(it => {
      const a = it.nombre.toLowerCase(), b = pur.nombre.toLowerCase();
      return b.split(' ').some(w => w.length > 3 && a.includes(w));
    });
    const { texto, v } = analizarLocal(nombre, val, pur.motivo, libre, sm, similares, metas, relapseMode);
    setAnalisis({ texto, v, val, similares, dias: toDays(val, sm) });
    setPurStep(3);
  };

  const registrarDec = (buena, label) => {
    addScore(buena ? 10 : -8, label);
    setPur({ nombre: '', valor: '', motivo: '' }); setAnalisis(null); setPurStep(0);
  };

  const toWishlist = () => {
    const val = parseInt(pur.valor.replace(/\D/g, '')) || 0;
    up({ ...perfil, wishlist: [{ id: uid(), nombre: pur.nombre, valor: val, motivo: pur.motivo, added: new Date().toISOString() }, ...(wishlist || [])] });
    addScore(8, `⏳ Pospuso: ${pur.nombre}`);
    setPur({ nombre: '', valor: '', motivo: '' }); setAnalisis(null); setPurStep(0);
  };

  const TABS = [
    { id: 'dashboard', icon: '🏠', label: 'Inicio' },
    { id: 'comprar',   icon: '🛑', label: '¿Lo necesito?' },
    { id: 'metas',     icon: '🎯', label: 'Metas' },
    { id: 'deudas',    icon: '📋', label: 'Deudas' },
    { id: 'score',     icon: '⭐', label: 'Score' },
    { id: 'ajustes',   icon: '⚙️', label: 'Ajustes' },
  ];

  const renderContent = () => {
    switch (tab) {

      case 'dashboard': return (
        <ScrollView contentContainerStyle={styles.tabContent}>
          <Text style={styles.pageTitle}>{relapseMode ? `⚠️ ${nombre}, cuidado` : `${nombre} ${level.icon}`}</Text>
          <Text style={styles.pageSubtitle}>{new Date().toLocaleDateString('es-CL', { weekday: 'long', day: 'numeric', month: 'long' })}{isNight() ? ' · 🌙 Horario de riesgo' : ''}{isWE() ? ' · 📅 Fin de semana' : ''}</Text>

          {relapseMode && <GCard accent={C.redBorder} style={{ backgroundColor: C.redBg, marginBottom: 12 }}>
            <Text style={[styles.alertText, { color: C.red }]}>Llevas {badStreak} malas decisiones. Estás entrando en desorden. Volvamos al control.</Text>
          </GCard>}

          {/* Botón saldo oculto */}
          <TouchableOpacity onPress={() => setShowSaldo(true)} style={styles.saldoBtn} activeOpacity={0.8}>
            <View>
              <Text style={styles.saldoBtnLabel}>💳 Tu dinero libre</Text>
              <Text style={styles.saldoBtnMonto}>$ • • • • •</Text>
              <Text style={styles.saldoBtnSub}>Toca para ver con PIN</Text>
            </View>
            <Text style={{ color: C.teal, fontSize: 22 }}>🔐</Text>
          </TouchableOpacity>

          <View style={styles.metricsRow}>
            <View style={styles.metric}><Text style={styles.metricLabel}>Sueldo</Text><Text style={[styles.metricValue, { color: C.teal }]}>{fmtS(sm)}</Text></View>
            <View style={styles.metric}><Text style={styles.metricLabel}>En deudas</Text><Text style={[styles.metricValue, { color: C.red }]}>{fmtS(totalD)}</Text><Text style={styles.metricSub}>{presion}%</Text></View>
          </View>

          <GCard>
            <Text style={styles.sectionTitle}>Presión financiera</Text>
            <MBar pct={presion} color={presion < 35 ? C.green : presion < 55 ? C.amber : C.red}/>
            <View style={styles.barLabels}>
              <Text style={{ color: C.muted, fontSize: 11 }}>Deudas {presion}%</Text>
              <Text style={{ color: presion < 35 ? C.green : presion < 55 ? C.amber : C.red, fontSize: 11, fontWeight: '700' }}>
                {presion < 35 ? 'Saludable 🟢' : presion < 55 ? 'Cuidado 🟡' : 'Alarma 🔴'}
              </Text>
            </View>
          </GCard>

          {activeMetas.length > 0 && <GCard style={{ backgroundColor: C.purpleBg, borderColor: '#3A2070' }}>
            <Text style={[styles.sectionTitle, { color: C.purple }]}>🎯 Metas activas</Text>
            {activeMetas.slice(0, 2).map(m => {
              const pct = Math.round(((m.montoActual || 0) / m.montoObj) * 100);
              return <View key={m.id} style={{ marginBottom: 10 }}>
                <View style={styles.metaRow}><Text style={{ color: C.text, fontSize: 13 }}>{m.nombre}</Text><Text style={{ color: C.purple, fontWeight: '700', fontSize: 12 }}>{pct}%</Text></View>
                <MBar pct={pct} color={C.purple}/>
                <Text style={styles.metaSub}>{fmt(m.montoActual || 0)} de {fmt(m.montoObj)}</Text>
              </View>;
            })}
          </GCard>}

          <GCard style={{ backgroundColor: C.tealBg, borderColor: C.tealBorder }}>
            <Text style={[styles.sectionTitle, { color: C.teal }]}>Costo real en tiempo</Text>
            {[[5000,'Comida del día'],[20000,'Cena para dos'],[50000,'Fin de semana']].map(([v,l],i) => (
              <Row key={i} label={`${l} (${fmt(v)})`} value={`${toHrs(v, sm)}h trabajo`} color={C.amber}/>
            ))}
          </GCard>

          <GBtn label="⚡ ¿Lo necesito? Analizar compra" variant="primary" full onPress={() => setTab('comprar')} style={{ marginTop: 4 }}/>
        </ScrollView>
      );

      case 'comprar': return (
        <ScrollView contentContainerStyle={styles.tabContent} keyboardShouldPersistTaps="handled">
          <Text style={styles.pageTitle}>¿Lo necesito de verdad?</Text>
          <Text style={styles.pageSubtitle}>{relapseMode ? '⚠️ Modo recaída — sé extra honesto' : 'El freno antes de gastar de más'}</Text>

          {purStep === 0 && <>
            {relapseMode && <GCard accent={C.redBorder} style={{ backgroundColor: C.redBg }}><Text style={[styles.alertText, { color: C.red }]}>Llevas {badStreak} malas decisiones. ¿Realmente necesitas comprar algo ahora?</Text></GCard>}
            <GCard>
              <Text style={styles.label}>¿Qué quieres comprar?</Text>
              <GInp placeholder="Ej: Zapatillas, celular, ropa..." value={pur.nombre} onChangeText={t => setPur({ ...pur, nombre: t })}/>
              <Text style={styles.label}>¿Cuánto cuesta?</Text>
              <GInp placeholder="Precio en pesos" value={pur.valor} onChangeText={t => setPur({ ...pur, valor: t })} keyboardType="numeric"/>
              {pur.valor && parseInt(pur.valor.replace(/\D/g, '')) > 0 && (
                <View style={[styles.infoBg, { marginTop: 8 }]}>
                  <Text style={{ color: C.amber, fontSize: 13 }}>Equivale a <Text style={{ fontWeight: '700' }}>{toDays(parseInt(pur.valor.replace(/\D/g, '')), sm)} días de trabajo</Text> · {toHrs(parseInt(pur.valor.replace(/\D/g, '')), sm)} horas</Text>
                </View>
              )}
              <Text style={styles.label}>¿Para qué lo necesitas? (sé honesto)</Text>
              <GInp placeholder="Ej: El mío se rompió / simplemente lo quiero..." value={pur.motivo} onChangeText={t => setPur({ ...pur, motivo: t })}/>
              {pur.valor && parseInt(pur.valor.replace(/\D/g, '')) > 0 && (
                <View style={styles.libreRow}>
                  <View><Text style={styles.libreLabel}>Tienes hoy</Text><Text style={[styles.libreMonto, { color: C.green }]}>{fmt(libre)}</Text></View>
                  <Text style={{ color: C.muted, fontSize: 20 }}>→</Text>
                  <View style={{ alignItems: 'flex-end' }}><Text style={styles.libreLabel}>Si compras</Text><Text style={[styles.libreMonto, { color: C.red }]}>{fmt(libre - (parseInt(pur.valor.replace(/\D/g, '')) || 0))}</Text></View>
                </View>
              )}
              <GBtn label="Analizar esta compra →" onPress={() => setPurStep(1)} disabled={!pur.nombre || !pur.valor} full style={{ marginTop: 12 }}/>
            </GCard>

            {/* Wishlist */}
            {(wishlist || []).length > 0 && <>
              <Text style={[styles.sectionTitle, { marginTop: 16 }]}>⏳ Lista de espera</Text>
              {(wishlist || []).map(w => {
                const dias = Math.floor((Date.now() - new Date(w.added)) / 864e5);
                return <GCard key={w.id}>
                  <View style={styles.wishRow}>
                    <View style={{ flex: 1 }}>
                      <Text style={styles.wishNombre}>{w.nombre}</Text>
                      <Text style={styles.wishMotivo}>{w.motivo || 'Sin razón'}</Text>
                      <Text style={{ color: dias >= 2 ? C.green : C.amber, fontSize: 11, marginTop: 4 }}>{dias === 0 ? 'Hoy' : `Hace ${dias} día/s`}</Text>
                      {dias >= 2 && <Text style={{ color: C.green, fontSize: 11, marginTop: 4 }}>✓ {dias} días sin comprarlo. ¿Aún lo quieres?</Text>}
                    </View>
                    <Text style={styles.wishValor}>{fmt(w.valor)}</Text>
                  </View>
                  <View style={styles.btnsRow}>
                    <GBtn label="Ya no lo quiero ✓" variant="green" onPress={() => { addScore(12, `✅ Desistió: ${w.nombre}`); up({ ...perfil, wishlist: (wishlist || []).filter(x => x.id !== w.id) }); }} style={{ flex: 1, marginRight: 6 }}/>
                    <GBtn label="Eliminar" variant="ghost" onPress={() => up({ ...perfil, wishlist: (wishlist || []).filter(x => x.id !== w.id) })} style={{ flex: 1 }}/>
                  </View>
                </GCard>;
              })}
            </>}
          </>}

          {purStep === 1 && (
            <View style={styles.frictionBox}>
              <Text style={styles.frictionStop}>🛑</Text>
              <Text style={styles.frictionTitle}>Espera {countdown} segundo{countdown !== 1 ? 's' : ''}</Text>
              <Text style={styles.frictionSub}>El 60% de los impulsos desaparecen en 10 segundos.</Text>
              <View style={styles.countCircle}><Text style={styles.countNum}>{countdown}</Text></View>
              <Text style={{ color: C.muted, fontSize: 12, marginTop: 12 }}>"{pur.nombre}" · {fmt(parseInt(pur.valor.replace(/\D/g, '')) || 0)}</Text>
              <GBtn label="← Cancelar" variant="ghost" onPress={() => setPurStep(0)} style={{ marginTop: 16 }}/>
            </View>
          )}

          {purStep === 2 && (
            <View>
              <Text style={styles.sectionTitle}>La realidad antes de decidir</Text>
              <GCard style={{ backgroundColor: C.amberBg, borderColor: C.amberBorder }}>
                <Text style={[styles.sectionTitle, { color: C.amber }]}>💰 Impacto financiero</Text>
                <Row label="Precio" value={fmt(parseInt(pur.valor.replace(/\D/g, '')) || 0)} color={C.amber} bold/>
                <Row label="Días de trabajo" value={`${toDays(parseInt(pur.valor.replace(/\D/g, '')) || 0, sm)} días`} color={C.amber}/>
                <Row label="Libre hoy" value={fmt(libre)}/>
                <Row label="Si compras, queda" value={fmt(libre - (parseInt(pur.valor.replace(/\D/g, '')) || 0))} color={libre - (parseInt(pur.valor.replace(/\D/g, '')) || 0) > 0 ? C.green : C.red} bold/>
              </GCard>
              <GBtn label="Ver análisis completo →" onPress={hacerAnalisis} full style={{ marginTop: 4 }}/>
              <GBtn label="← Cancelar" variant="ghost" onPress={() => setPurStep(0)} style={{ marginTop: 8 }}/>
            </View>
          )}

          {purStep === 3 && analisis && (() => {
            const vColors = { verde: { bg: C.greenBg, border: C.greenBorder, color: C.green, icon: '✓' }, amarillo: { bg: C.amberBg, border: C.amberBorder, color: C.amber, icon: '!' }, rojo: { bg: C.redBg, border: C.redBorder, color: C.red, icon: '✕' } };
            const vs = vColors[analisis.v] || vColors.amarillo;
            return <View>
              <GCard style={{ backgroundColor: vs.bg, borderColor: vs.border }}>
                <View style={styles.veredictoHeader}>
                  <View style={[styles.veredictoIcon, { backgroundColor: vs.color }]}><Text style={{ color: C.bg, fontWeight: '900', fontSize: 18 }}>{vs.icon}</Text></View>
                  <Text style={[styles.veredictoTitle, { color: vs.color }]}>{analisis.v.toUpperCase()}</Text>
                </View>
                {analisis.similares?.length > 0 && <GCard style={{ backgroundColor: C.amberBg, borderColor: C.amberBorder, marginBottom: 10 }}>
                  <Text style={{ color: C.amber, fontWeight: '700', fontSize: 12, marginBottom: 4 }}>📦 Ya tienes algo similar:</Text>
                  {analisis.similares.map((s, i) => <Text key={i} style={{ color: C.text, fontSize: 12 }}>{s.nombre} · ×{s.cantidad}</Text>)}
                </GCard>}
                <Text style={styles.analisisText}>{analisis.texto}</Text>
                <View style={styles.analisisMetrics}>
                  {[['Precio', fmt(analisis.val)], ['Días', `${analisis.dias}d`], ['Quedaría', fmtS(libre - analisis.val)]].map(([l, v]) => (
                    <View key={l} style={styles.analisisMetric}><Text style={styles.analisisMetricLabel}>{l}</Text><Text style={[styles.analisisMetricVal, { color: vs.color }]}>{v}</Text></View>
                  ))}
                </View>
                <View style={styles.btnsRow}>
                  <GBtn label="Comprar" variant="danger" onPress={() => registrarDec(false, `⚠️ Compró: ${pur.nombre}`)} style={{ flex: 1, marginRight: 4 }}/>
                  <GBtn label="⏳ Esperar" variant="amber" onPress={toWishlist} style={{ flex: 1, marginRight: 4 }}/>
                  <GBtn label="✓ No compro" variant="green" onPress={() => registrarDec(true, `✅ Evitó: ${pur.nombre}`)} style={{ flex: 1 }}/>
                </View>
              </GCard>
              <GBtn label="← Nueva consulta" variant="ghost" onPress={() => setPurStep(0)} style={{ marginTop: 4 }}/>
            </View>;
          })()}
        </ScrollView>
      );

      case 'metas': return (
        <ScrollView contentContainerStyle={styles.tabContent}>
          <Text style={styles.pageTitle}>Sistema de Metas</Text>
          <View style={styles.metricsRow}>
            <View style={styles.metric}><Text style={styles.metricLabel}>Activas</Text><Text style={[styles.metricValue, { color: C.purple }]}>{activeMetas.length}</Text></View>
            <View style={styles.metric}><Text style={styles.metricLabel}>Completadas</Text><Text style={[styles.metricValue, { color: C.green }]}>{(metas || []).filter(m => m.completada).length}</Text></View>
          </View>
          {(metas || []).map(m => {
            const pct = Math.min(100, Math.round(((m.montoActual || 0) / m.montoObj) * 100));
            const dL = sm > 0 ? Math.ceil((m.montoObj - (m.montoActual || 0)) / (sm / 30)) : 999;
            return <GCard key={m.id} accent={m.completada ? C.greenBorder : undefined} style={{ backgroundColor: m.completada ? C.greenBg : C.card }}>
              <View style={styles.metaHeader}>
                <View style={{ flex: 1 }}>
                  <Text style={[styles.metaNombre, { color: m.completada ? C.green : C.text }]}>{m.nombre}{m.completada ? ' ✓' : ''}</Text>
                  <Text style={styles.metaSub}>Prioridad: {m.prioridad}</Text>
                </View>
                <View style={styles.metaRight}>
                  {!m.completada && <View style={[styles.badge, { backgroundColor: pct >= 100 ? C.greenBg : pct >= 50 ? C.tealBg : C.amberBg }]}><Text style={{ color: pct >= 100 ? C.green : pct >= 50 ? C.teal : C.amber, fontSize: 11, fontWeight: '700' }}>{pct}%</Text></View>}
                  <TouchableOpacity onPress={() => up({ ...perfil, metas: (metas || []).filter(x => x.id !== m.id) })}><Text style={{ color: C.muted, fontSize: 20, marginLeft: 8 }}>×</Text></TouchableOpacity>
                </View>
              </View>
              <MBar pct={pct} color={pct >= 100 ? C.green : C.purple}/>
              <View style={styles.metaFooter}>
                <Text style={styles.metaSub}>{fmt(m.montoActual || 0)} de {fmt(m.montoObj)}</Text>
                {!m.completada && <Text style={styles.metaSub}>~{dL} días</Text>}
              </View>
              {pct >= 100 && !m.completada && <GBtn label="🎉 ¡Marcar completada!" variant="green" full onPress={() => { const np = { ...perfil, metas: (metas || []).map(x => x.id === m.id ? { ...x, completada: true } : x) }; up(np); addScore(20, `🏆 Meta cumplida: ${m.nombre}`); }} style={{ marginTop: 8 }}/>}
            </GCard>;
          })}
          <TouchableOpacity onPress={() => setShowForms({ ...showForms, meta: !showForms.meta })} style={styles.addBtn}>
            <Text style={{ color: C.muted, fontSize: 14 }}>🎯 + Nueva meta</Text>
          </TouchableOpacity>
          {showForms.meta && <GCard>
            <Text style={styles.label}>¿Qué quieres lograr?</Text>
            <GInp placeholder="Fondo emergencia, viaje, auto..." value={newMeta.nombre} onChangeText={t => setNewMeta({ ...newMeta, nombre: t })}/>
            <Text style={styles.label}>Monto objetivo</Text>
            <GInp placeholder="Ej: 1500000" value={newMeta.montoObj} onChangeText={t => setNewMeta({ ...newMeta, montoObj: t })} keyboardType="numeric"/>
            <Text style={styles.label}>Ya tienes ahorrado</Text>
            <GInp placeholder="0" value={newMeta.montoActual} onChangeText={t => setNewMeta({ ...newMeta, montoActual: t })} keyboardType="numeric"/>
            <View style={styles.btnsRow}>
              <GBtn label="Guardar" onPress={() => { if (!newMeta.nombre || !newMeta.montoObj) return; const mO = parseInt(newMeta.montoObj.replace(/\D/g, '')) || 0; const mA = parseInt(newMeta.montoActual.replace(/\D/g, '')) || 0; up({ ...perfil, metas: [...(metas || []), { id: uid(), nombre: newMeta.nombre, montoObj: mO, montoActual: mA, prioridad: 'media', completada: false }] }); setNewMeta({ nombre: '', montoObj: '', montoActual: '' }); setShowForms({ ...showForms, meta: false }); addScore(5, '🎯 Nueva meta'); }} style={{ flex: 1, marginRight: 6 }}/>
              <GBtn label="Cancelar" variant="ghost" onPress={() => setShowForms({ ...showForms, meta: false })} style={{ flex: 1 }}/>
            </View>
          </GCard>}
        </ScrollView>
      );

      case 'deudas': return (
        <ScrollView contentContainerStyle={styles.tabContent}>
          <Text style={styles.pageTitle}>Módulo de deudas</Text>
          <View style={styles.metricsRow}>
            <View style={styles.metric}><Text style={styles.metricLabel}>Total mensual</Text><Text style={[styles.metricValue, { color: C.red }]}>{fmt(totalD)}</Text></View>
            <View style={styles.metric}><Text style={styles.metricLabel}>Días perdidos</Text><Text style={[styles.metricValue, { color: C.amber }]}>{toDays(totalD, sm)}d</Text></View>
          </View>
          <GCard style={{ backgroundColor: C.redBg, borderColor: C.redBorder }}>
            <Text style={[styles.alertText, { color: C.red }]}>⏱ Tus deudas te quitan <Text style={{ fontWeight: '700' }}>{toDays(totalD, sm)} días de trabajo</Text> al mes antes de que los veas.</Text>
          </GCard>
          {debts.map(d => <GCard key={d.id}>
            <View style={styles.debtRow}>
              <View style={{ flex: 1 }}><Text style={styles.debtNombre}>{d.nombre}</Text><Text style={styles.debtSub}>Quita {toDays(d.cuota, sm)} días/mes de libertad</Text></View>
              <View style={{ alignItems: 'flex-end', flexDirection: 'row', gap: 8 }}>
                <Text style={[styles.debtCuota, { color: C.red }]}>{fmt(d.cuota)}<Text style={{ fontSize: 10, color: C.muted }}>/mes</Text></Text>
                <TouchableOpacity onPress={() => up({ ...perfil, debts: debts.filter(x => x.id !== d.id) })}><Text style={{ color: C.muted, fontSize: 20 }}>×</Text></TouchableOpacity>
              </View>
            </View>
            <MBar pct={totalD > 0 ? (d.cuota / totalD) * 100 : 0} color={C.red}/>
          </GCard>)}
          <TouchableOpacity onPress={() => setShowForms({ ...showForms, debt: !showForms.debt })} style={styles.addBtn}>
            <Text style={{ color: C.muted, fontSize: 14 }}>+ Agregar deuda</Text>
          </TouchableOpacity>
          {showForms.debt && <GCard>
            <Text style={styles.label}>Nombre</Text>
            <GInp placeholder="Ej: Tarjeta BCI" value={newDebt.nombre} onChangeText={t => setNewDebt({ ...newDebt, nombre: t })}/>
            <Text style={styles.label}>Cuota mensual</Text>
            <GInp placeholder="Ej: 150000" value={newDebt.cuota} onChangeText={t => setNewDebt({ ...newDebt, cuota: t })} keyboardType="numeric"/>
            <View style={styles.btnsRow}>
              <GBtn label="Guardar" onPress={() => { if (!newDebt.nombre || !newDebt.cuota) return; up({ ...perfil, debts: [...debts, { id: uid(), nombre: newDebt.nombre, cuota: parseInt(newDebt.cuota.replace(/\D/g, '')) || 0 }] }); setNewDebt({ nombre: '', cuota: '' }); setShowForms({ ...showForms, debt: false }); }} style={{ flex: 1, marginRight: 6 }}/>
              <GBtn label="Cancelar" variant="ghost" onPress={() => setShowForms({ ...showForms, debt: false })} style={{ flex: 1 }}/>
            </View>
          </GCard>}
        </ScrollView>
      );

      case 'score': return (
        <ScrollView contentContainerStyle={styles.tabContent}>
          <Text style={styles.pageTitle}>Score de disciplina</Text>
          <GCard style={{ alignItems: 'center' }}>
            <Text style={{ fontSize: 50, marginBottom: 4 }}>{level.icon}</Text>
            <Text style={[styles.scorNum, { color: level.color }]}>{score}</Text>
            <Text style={{ color: C.muted, fontSize: 12, marginBottom: 8 }}>de 100 puntos</Text>
            <Text style={[styles.scorLabel, { color: level.color }]}>{level.label}</Text>
            <MBar pct={score} color={level.color} height={8}/>
          </GCard>
          <GCard>
            <Text style={styles.sectionTitle}>Decisiones inteligentes</Text>
            <Row label="Compras evitadas" value={savedDec.length} color={C.green}/>
            <Row label="Metas activas" value={activeMetas.length} color={C.purple}/>
            <Row label="Score actual" value={`${score}/100`} color={level.color} bold/>
          </GCard>
          {history.length > 0 && <GCard>
            <Text style={styles.sectionTitle}>Últimas decisiones</Text>
            {history.slice(0, 8).map(h => <View key={h.id} style={styles.histRow}>
              <Text style={{ color: C.text, fontSize: 12, flex: 1 }}>{h.reason}</Text>
              <Text style={{ color: h.delta > 0 ? C.green : C.red, fontWeight: '700', fontSize: 13 }}>{h.delta > 0 ? '+' : ''}{h.delta}</Text>
            </View>)}
          </GCard>}
        </ScrollView>
      );

      case 'ajustes': return (
        <ScrollView contentContainerStyle={styles.tabContent}>
          <Text style={styles.pageTitle}>Ajustes</Text>

          <GCard>
            <Text style={styles.sectionTitle}>⚙️ Sueldo mensual</Text>
            {editingS ? <>
              <GInp placeholder={`Sueldo actual: ${fmt(sm)}`} value={editSueldo} onChangeText={setEditSueldo} keyboardType="numeric"/>
              <View style={[styles.btnsRow, { marginTop: 10 }]}>
                <GBtn label="Guardar" onPress={() => { const ns = parseInt(editSueldo.replace(/\D/g, '')) || sm; up({ ...perfil, sueldoMensual: ns }); setEditingS(false); setEditSueldo(''); }} style={{ flex: 1, marginRight: 6 }}/>
                <GBtn label="Cancelar" variant="ghost" onPress={() => setEditingS(false)} style={{ flex: 1 }}/>
              </View>
            </> : <View style={styles.sueldoRow}>
              <Text style={[styles.metricValue, { color: C.teal }]}>{fmt(sm)}/mes</Text>
              <GBtn label="Editar" variant="ghost" onPress={() => { setEditingS(true); setEditSueldo(sm.toString()); }}/>
            </View>}
          </GCard>

          <GCard>
            <Text style={styles.sectionTitle}>🔐 PIN de seguridad</Text>
            <Text style={styles.pageSubtitle}>{pin ? '✅ PIN configurado' : 'Sin PIN — el saldo está desprotegido'}</Text>
            <GBtn label={pin ? 'Cambiar PIN' : 'Crear PIN'} variant={pin ? 'ghost' : 'primary'} onPress={() => setShowSetPin(true)} style={{ marginTop: 8 }}/>
            {pin && <GBtn label="Eliminar PIN" variant="danger" onPress={() => { Alert.alert('¿Eliminar PIN?', 'El saldo quedará visible sin protección.', [{ text: 'Cancelar' }, { text: 'Eliminar', onPress: () => up({ ...perfil, pin: null }) }]); }} style={{ marginTop: 6 }}/>}
          </GCard>

          <GCard>
            <Text style={styles.sectionTitle}>⏰ Recordatorios</Text>
            <Text style={styles.pageSubtitle}>Cada cuántas horas te recordamos revisar tus finanzas</Text>
            <View style={styles.reminderGrid}>
              {REMINDER_OPTIONS.map(h => (
                <TouchableOpacity key={h} onPress={() => up({ ...perfil, reminderHours: h })}
                  style={[styles.reminderBtn, reminderHours === h && styles.reminderBtnActive]}>
                  <Text style={[styles.reminderText, reminderHours === h && styles.reminderTextActive]}>{h}h</Text>
                </TouchableOpacity>
              ))}
            </View>
            <Text style={styles.pageSubtitle}>Activo cada {reminderHours} horas ✓</Text>
            <Text style={{ color: C.muted, fontSize: 11, marginTop: 4 }}>Nota: Las notificaciones automáticas requieren la versión compilada de la app (APK).</Text>
          </GCard>

          <GCard>
            <Text style={styles.sectionTitle}>📧 Tu correo</Text>
            <Text style={styles.pageSubtitle}>Para recibir tu historial y estado de cuenta</Text>
            {editingS && editSueldo === 'email' ? (
              <View>
                <GInp placeholder="tucorreo@gmail.com" value={perfil.email || ''} onChangeText={t => up({ ...perfil, email: t })} keyboardType="email-address"/>
                <View style={[styles.btnsRow, { marginTop: 10 }]}>
                  <GBtn label="Guardar" onPress={() => { setEditingS(false); setEditSueldo(''); Alert.alert('✅ Correo guardado', `Historial se enviará a ${perfil.email}`); }} style={{ flex: 1, marginRight: 6 }}/>
                  <GBtn label="Cancelar" variant="ghost" onPress={() => { setEditingS(false); setEditSueldo(''); }} style={{ flex: 1 }}/>
                </View>
              </View>
            ) : (
              <View style={styles.sueldoRow}>
                <Text style={{ color: perfil.email ? C.text : C.muted, fontSize: 14 }}>{perfil.email || 'Sin correo configurado'}</Text>
                <GBtn label={perfil.email ? 'Editar' : 'Agregar'} variant="ghost" onPress={() => { setEditingS(true); setEditSueldo('email'); }}/>
              </View>
            )}
            {perfil.email && (
              <GBtn label="📤 Enviarme el historial ahora" variant="primary" full onPress={() => Alert.alert('📧 Historial', `Se enviará un resumen a:\n${perfil.email}\n\n(Función completa disponible en la versión con backend)`)} style={{ marginTop: 10 }}/>
            )}
          </GCard>

          <GCard style={{ backgroundColor: C.tealBg, borderColor: C.tealBorder }}>
            <Text style={[styles.sectionTitle, { color: C.teal }]}>📤 Exportar datos</Text>
            <GBtn label="Generar código de respaldo" onPress={() => { setShareCode(JSON.stringify({ ...perfil, exportedAt: new Date().toISOString() }).slice(0, 100) + '...'); Alert.alert('Datos exportados', 'Ve a Ajustes de tu teléfono para copiar el código de respaldo.'); }}/>
          </GCard>

          <GCard style={{ backgroundColor: C.redBg, borderColor: C.redBorder }}>
            <Text style={[styles.sectionTitle, { color: C.red }]}>⚠️ Zona peligrosa</Text>
            <GBtn label="Resetear todo" variant="danger" onPress={() => Alert.alert('¿Seguro?', 'Se borrarán todos tus datos.', [{ text: 'Cancelar' }, { text: 'Borrar todo', style: 'destructive', onPress: async () => { await AsyncStorage.clear(); setPerfil(null); setNombre(null); } }])}/>
          </GCard>

          <View style={{ alignItems: 'center', marginTop: 20, paddingBottom: 20 }}>
            <Text style={{ fontSize: 28 }}>🛑</Text>
            <Text style={{ color: C.teal, fontSize: 20, fontWeight: '900', marginTop: 6 }}>GASTO CERO</Text>
            <Text style={{ color: C.muted, fontSize: 12, marginTop: 4, textAlign: 'center' }}>La app que te frena antes de gastar de más</Text>
            <View style={{ height: 1, backgroundColor: C.border, width: '80%', marginVertical: 12 }}/>
            <Text style={{ color: C.muted, fontSize: 11, textAlign: 'center' }}>Creada y dirigida por</Text>
            <Text style={{ color: C.teal, fontSize: 14, fontWeight: '700', marginTop: 2 }}>Juan Colombia</Text>
            <Text style={{ color: C.text, fontSize: 13, marginTop: 2 }}>Juan Manuel Villegas</Text>
            <View style={{ height: 1, backgroundColor: C.border, width: '80%', marginVertical: 12 }}/>
            <Text style={{ color: C.muted, fontSize: 10 }}>v1.0 · React Native · 100% gratis</Text>
          </View>
        </ScrollView>
      );

      default: return null;
    }
  };

  return (
    <View style={styles.appContainer}>
      <StatusBar barStyle="light-content" backgroundColor={C.bg}/>

      {/* Modal saldo */}
      <Modal visible={showSaldo} animationType="slide" presentationStyle="fullScreen">
        <SaldoOculto libre={libre} sm={sm} nombre={nombre} pin={pin} onSetPin={() => { setShowSaldo(false); setShowSetPin(true); }} onClose={() => setShowSaldo(false)}/>
      </Modal>

      {/* Modal crear PIN */}
      <Modal visible={showSetPin} animationType="slide" presentationStyle="fullScreen">
        <PinScreen creating onSuccess={p => { up({ ...perfil, pin: p }); setShowSetPin(false); Alert.alert('✅ PIN creado', 'Tu saldo ahora está protegido.'); }} onCancel={() => setShowSetPin(false)}/>
      </Modal>

      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerLeft}>
          <Text style={styles.headerLogo}>🛑</Text>
          <View>
            <Text style={styles.headerTitle}>GASTO CERO</Text>
            <Text style={styles.headerSub}>{nombre} · {level.icon} {level.label}</Text>
          </View>
        </View>
        <TouchableOpacity onPress={() => setShowSaldo(true)} style={styles.saldoBtnMini}>
          <Text style={styles.saldoBtnMiniText}>💳 {fmt(libre)}</Text>
          <Text style={styles.saldoBtnMiniSub}>🔐 Ver</Text>
        </TouchableOpacity>
      </View>

      {/* Content */}
      <View style={{ flex: 1 }}>{renderContent()}</View>

      {/* Bottom Nav */}
      <View style={styles.bottomNav}>
        {TABS.map(t => (
          <TouchableOpacity key={t.id} onPress={() => setTab(t.id)} style={styles.navItem}>
            <Text style={[styles.navIcon, tab === t.id && { color: C.teal }]}>{t.icon}</Text>
            <Text style={[styles.navLabel, tab === t.id && { color: C.teal, fontWeight: '700' }]}>{t.label}</Text>
          </TouchableOpacity>
        ))}
      </View>
    </View>
  );
}

// ═══════════════════════════════════════════════════════════════════════════
// ESTILOS
// ═══════════════════════════════════════════════════════════════════════════
const { width } = Dimensions.get('window');
const styles = StyleSheet.create({
  appContainer: { flex: 1, backgroundColor: C.bg },
  screen: { flex: 1, backgroundColor: C.bg },
  center: { flexGrow: 1, justifyContent: 'center', alignItems: 'center', padding: 20 },
  tabContent: { padding: 16, paddingBottom: 40 },
  card: { backgroundColor: C.card, borderRadius: 16, padding: 16, marginBottom: 12, borderWidth: 1, borderColor: C.border },
  btn: { borderRadius: 12, paddingVertical: 13, paddingHorizontal: 20, alignItems: 'center', justifyContent: 'center', borderWidth: 1 },
  btnText: { fontSize: 15, fontWeight: '700' },
  input: { backgroundColor: C.bg, borderWidth: 1, borderColor: C.border, borderRadius: 10, padding: 13, fontSize: 16, color: C.text, marginBottom: 4 },
  barBg: { backgroundColor: C.faint, borderRadius: 4, overflow: 'hidden' },
  barFill: { borderRadius: 4 },
  row: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingVertical: 8, borderBottomWidth: 1, borderBottomColor: C.border },
  rowLabel: { color: C.muted, fontSize: 13 },
  rowValue: { color: C.text, fontSize: 13, fontWeight: '500' },
  // Logo/Welcome
  logoBox: { alignItems: 'center', marginBottom: 24 },
  logoEmoji: { fontSize: 56, marginBottom: 8 },
  logoTitle: { fontSize: 28, fontWeight: '900', color: C.teal, letterSpacing: -1 },
  logoSub: { fontSize: 13, color: C.muted, marginTop: 4, textAlign: 'center' },
  featureRow: { flexDirection: 'row', alignItems: 'center', backgroundColor: C.card, borderRadius: 12, padding: 12, marginBottom: 8, borderWidth: 1, borderColor: C.border, width: '100%' },
  featureIcon: { fontSize: 18, marginRight: 10 },
  featureText: { color: C.text, fontSize: 13, flex: 1 },
  disclaimer: { color: C.muted, fontSize: 11, marginTop: 12 },
  label: { color: C.muted, fontSize: 13, marginBottom: 6, marginTop: 12 },
  infoBg: { backgroundColor: C.tealBg, borderRadius: 10, padding: 12, borderWidth: 1, borderColor: C.tealBorder },
  infoLabel: { color: C.muted, fontSize: 11 },
  infoValue: { color: C.teal, fontSize: 22, fontWeight: '800' },
  infoSub: { color: C.muted, fontSize: 11, marginTop: 2 },
  // Frecuencia
  frecRow: { flexDirection: 'row', gap: 8, marginBottom: 4 },
  frecBtn: { flex: 1, paddingVertical: 10, alignItems: 'center', borderRadius: 10, borderWidth: 1, borderColor: C.border, backgroundColor: 'transparent' },
  frecBtnActive: { backgroundColor: C.tealBg, borderColor: C.teal },
  frecText: { color: C.muted, fontSize: 12 },
  frecTextActive: { color: C.teal, fontWeight: '700' },
  // Header
  header: { backgroundColor: C.card, borderBottomWidth: 1, borderBottomColor: C.border, paddingHorizontal: 16, paddingTop: Platform.OS === 'android' ? StatusBar.currentHeight + 8 : 48, paddingBottom: 12, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  headerLeft: { flexDirection: 'row', alignItems: 'center', gap: 10 },
  headerLogo: { fontSize: 24 },
  headerTitle: { fontSize: 14, fontWeight: '900', color: C.teal },
  headerSub: { fontSize: 10, color: C.muted },
  // Saldo mini en header
  saldoBtnMini: { backgroundColor: C.tealBg, borderRadius: 10, padding: 8, alignItems: 'center', borderWidth: 1, borderColor: C.tealBorder },
  saldoBtnMiniText: { color: C.teal, fontSize: 12, fontWeight: '700' },
  saldoBtnMiniSub: { color: C.muted, fontSize: 10 },
  // Saldo pantalla
  saldoHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 },
  saldoNombre: { fontSize: 18, fontWeight: '800', color: C.text },
  saldoLabel: { color: C.muted, fontSize: 13, marginBottom: 8 },
  saldoMonto: { fontSize: 36, fontWeight: '900' },
  saldoDias: { color: C.muted, fontSize: 12, marginTop: 4 },
  saldoOculto: { fontSize: 32, fontWeight: '700', color: C.muted, letterSpacing: 4 },
  // Dashboard
  saldoBtn: { backgroundColor: C.card, borderRadius: 16, padding: 16, marginBottom: 12, borderWidth: 1, borderColor: C.tealBorder, flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  saldoBtnLabel: { color: C.muted, fontSize: 12 },
  saldoBtnMonto: { color: C.text, fontSize: 24, fontWeight: '800', letterSpacing: 2 },
  saldoBtnSub: { color: C.teal, fontSize: 11 },
  metricsRow: { flexDirection: 'row', gap: 10, marginBottom: 12 },
  metric: { flex: 1, backgroundColor: C.card2, borderRadius: 14, padding: 14 },
  metricLabel: { color: C.muted, fontSize: 11, marginBottom: 3 },
  metricValue: { fontSize: 20, fontWeight: '800', color: C.text },
  metricSub: { color: C.muted, fontSize: 10, marginTop: 2 },
  barLabels: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 6 },
  alertText: { fontSize: 13, lineHeight: 20 },
  sectionTitle: { fontSize: 14, fontWeight: '700', color: C.text, marginBottom: 10 },
  metaRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 4 },
  metaSub: { color: C.muted, fontSize: 10, marginTop: 4 },
  pageTitle: { fontSize: 18, fontWeight: '800', color: C.text, marginBottom: 4 },
  pageSubtitle: { fontSize: 12, color: C.muted, marginBottom: 14 },
  // Metas
  metaHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 },
  metaNombre: { fontSize: 14, fontWeight: '700' },
  metaRight: { flexDirection: 'row', alignItems: 'center' },
  metaFooter: { flexDirection: 'row', justifyContent: 'space-between', marginTop: 5 },
  badge: { borderRadius: 20, paddingHorizontal: 8, paddingVertical: 2 },
  // Deudas
  debtRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 },
  debtNombre: { color: C.text, fontSize: 14, fontWeight: '700' },
  debtSub: { color: C.amber, fontSize: 11, marginTop: 3 },
  debtCuota: { fontSize: 16, fontWeight: '800' },
  // Comprar
  frictionBox: { alignItems: 'center', paddingVertical: 40 },
  frictionStop: { fontSize: 56, marginBottom: 12 },
  frictionTitle: { fontSize: 22, fontWeight: '800', color: C.text, marginBottom: 8 },
  frictionSub: { fontSize: 13, color: C.muted, textAlign: 'center', marginBottom: 24 },
  countCircle: { width: 90, height: 90, borderRadius: 45, backgroundColor: C.tealBg, borderWidth: 3, borderColor: C.teal, alignItems: 'center', justifyContent: 'center' },
  countNum: { fontSize: 36, fontWeight: '900', color: C.teal },
  libreRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', backgroundColor: C.card2, borderRadius: 12, padding: 12, marginTop: 10 },
  libreLabel: { color: C.muted, fontSize: 10 },
  libreMonto: { fontSize: 16, fontWeight: '700' },
  veredictoHeader: { flexDirection: 'row', alignItems: 'center', marginBottom: 12, gap: 10 },
  veredictoIcon: { width: 36, height: 36, borderRadius: 18, alignItems: 'center', justifyContent: 'center' },
  veredictoTitle: { fontSize: 16, fontWeight: '800' },
  analisisText: { fontSize: 14, color: C.text, lineHeight: 22, marginBottom: 12 },
  analisisMetrics: { flexDirection: 'row', gap: 8, marginBottom: 12 },
  analisisMetric: { flex: 1, backgroundColor: C.card, borderRadius: 10, padding: 10 },
  analisisMetricLabel: { color: C.muted, fontSize: 10 },
  analisisMetricVal: { fontSize: 13, fontWeight: '700' },
  // Wishlist
  wishRow: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 },
  wishNombre: { color: C.text, fontSize: 14, fontWeight: '700' },
  wishMotivo: { color: C.muted, fontSize: 11 },
  wishValor: { color: C.amber, fontSize: 16, fontWeight: '800' },
  btnsRow: { flexDirection: 'row', gap: 6, marginTop: 10 },
  addBtn: { borderWidth: 1, borderStyle: 'dashed', borderColor: C.border, borderRadius: 12, padding: 14, alignItems: 'center', marginBottom: 10 },
  // Ajustes
  sueldoRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  reminderGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginTop: 8, marginBottom: 8 },
  reminderBtn: { paddingVertical: 8, paddingHorizontal: 16, borderRadius: 20, borderWidth: 1, borderColor: C.border, backgroundColor: 'transparent' },
  reminderBtnActive: { backgroundColor: C.tealBg, borderColor: C.teal },
  reminderText: { color: C.muted, fontSize: 13 },
  reminderTextActive: { color: C.teal, fontWeight: '700' },
  // Score
  scorNum: { fontSize: 52, fontWeight: '900' },
  scorLabel: { fontSize: 16, fontWeight: '700', marginBottom: 10 },
  histRow: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingVertical: 6, borderBottomWidth: 1, borderBottomColor: C.border },
  // PIN
  pinTitle: { fontSize: 18, fontWeight: '800', color: C.text, marginBottom: 24, textAlign: 'center' },
  pinDots: { flexDirection: 'row', gap: 16, marginBottom: 40 },
  pinDot: { width: 16, height: 16, borderRadius: 8, borderWidth: 2, borderColor: C.teal, backgroundColor: 'transparent' },
  pinDotFilled: { backgroundColor: C.teal },
  pinGrid: { flexDirection: 'row', flexWrap: 'wrap', width: 240, gap: 12 },
  pinKey: { width: 68, height: 68, borderRadius: 34, backgroundColor: C.card, borderWidth: 1, borderColor: C.border, alignItems: 'center', justifyContent: 'center' },
  pinKeyEmpty: { backgroundColor: 'transparent', borderColor: 'transparent' },
  pinKeyText: { color: C.text, fontSize: 22, fontWeight: '700' },
  // Bottom nav
  bottomNav: { flexDirection: 'row', backgroundColor: C.card, borderTopWidth: 1, borderTopColor: C.border, paddingBottom: Platform.OS === 'ios' ? 24 : 10, paddingTop: 10 },
  navItem: { flex: 1, alignItems: 'center', gap: 4 },
  navIcon: { fontSize: 24, color: C.muted },
  navLabel: { fontSize: 11, color: C.muted },
});
