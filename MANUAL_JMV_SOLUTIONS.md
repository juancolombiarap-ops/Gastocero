# 🔧 MANUAL JMV SOLUTIONS — Sesión de Vehículos / KESS

> Documento de respaldo. Aquí está TODO lo configurado, para no depender de
> recordar ninguna conversación. Guárdalo y consérvalo.

---

## 1. Usuario de Windows dedicado

- **Usuario:** `JMV SOLUTIONS` (cuenta local, **administrador**)
- **Acceso:** PIN + preguntas de recuperación configuradas
- **Para qué:** sesión aparte, solo para mecánica / electromecánica de vehículos,
  separada del usuario principal (`ville`).
- Si olvidas el PIN → en el login click **"He olvidado mi PIN"** → pide la
  **contraseña** de la cuenta para resetearlo (ten la contraseña a mano).

---

## 2. La Máquina Virtual del KESS (lo más importante)

| Dato | Valor |
|---|---|
| Nombre de la VM | **Win7-32** |
| Snapshot bueno | **KSuite-listo** (Win7 + KSuite + driver KESS funcionando) |
| Sistema | Windows 7 Pro (32-bit), 2048 MB RAM, 2 CPU, disco 40 GB |
| Ubicación del archivo | `C:\VMs\Win7-32\Win7-32.vbox` |
| Login dentro del Windows 7 | usuario **juan** / contraseña **kess1234** |
| Software instalado | **KSuite 2.80** + driver del **KESS V2** (clon "Master Version") |
| KESS por USB | dispositivo FTDI **0403:b470** — se auto-captura por el filtro USB |

### Cómo agregar la VM (solo la 1ª vez en un usuario)
VirtualBox → **Máquina → Agregar** → seleccionar `C:\VMs\Win7-32\Win7-32.vbox`

---

## 3. ⚠️ REGLAS DE ORO (NO romper)

1. **OFFLINE SIEMPRE.** La VM NO debe tener internet.
   - Ya quedó con el **adaptador de red DESHABILITADO** (mejor opción).
   - Si KSuite dice **"Connection not established"** → **es NORMAL** offline.
   - 🚫 Si le das internet, KSuite se actualiza y **DAÑA (brickea) el KESS clon**.

2. **NUNCA arrancar la misma VM en dos usuarios a la vez** (`ville` y `JMV`)
   → corrompe el disco. Una sesión a la vez.

3. **El KESS va por USB, no por red.** USB sí, internet nunca.

4. Para **soltar el mouse/teclado** de la VM → tecla **Ctrl derecho**.

---

## 4. Cómo trabajar (paso a paso)

1. Entrar a la sesión de Windows **JMV SOLUTIONS** (con el PIN).
2. Abrir **VirtualBox** → seleccionar **Win7-32 (KSuite-listo)** → **Iniciar** ▶️.
   - Si sale "Windows Error Recovery" → elegir **Start Windows Normally** (normal).
   - Si pregunta por borrar archivos de instalación sobrantes → **Eliminar** (seguro).
3. Login del Windows 7: **juan / kess1234**.
4. Conectar el **KESS por USB** → se captura solo.
5. Abrir **KSuite** y trabajar. ("Connection not established" = normal).

---

## 5. Pendiente

- [ ] **Instalar GODIAG** (programa adicional). Falta definir: ¿está en el CD de
      instaladores, en USB, o se descarga? ¿Es para un equipo GODIAG físico o
      solo software?
- [ ] Verificar que KSuite **detecta el KESS** al conectarlo por USB.

---

## 6. Recuperar la conversación original de Claude Code

Esta configuración se hizo en **Claude Code de escritorio**, en el usuario `ville`.
Para retomar ese hilo con todo el contexto:

1. Abrir **PowerShell** en la laptop (usuario `ville`).
2. Ejecutar:
   ```
   claude --resume 75eda182-ec09-4763-b2a2-77d5627cf557
   ```

> Nota: las conversaciones de Claude Code se guardan **por usuario de Windows**.
> Lo que se hace en `ville` no aparece en `JMV SOLUTIONS` (cada uno tiene su
> propio historial).

---

_Última actualización: 2026-06-19_
