import { useState } from 'react'
import VictimApp from './apps/victim/VictimApp'
import ResponderApp from './apps/responder/ResponderApp'
import SupervisorApp from './apps/supervisor/SupervisorApp'
import {
  BellRing,
  ShieldCheck,
  Monitor,
  ArrowLeft,
  WifiOff,
  Radio,
  Cpu,
  Layers,
  RotateCcw,
  CheckCircle2,
  ChevronRight,
  Info
} from 'lucide-react'
import { api } from './api'

const PHONE_W = 390
const PHONE_H = 760

function PhoneFrame({ children }) {
  return (
    <div
      className="relative rounded-[48px] overflow-hidden shadow-2xl"
      style={{
        width: PHONE_W,
        height: PHONE_H,
        maxHeight: '85vh',
        background: '#F5F1EB',
        border: `2px solid #E5E0D8`,
        boxShadow: '0 32px 64px rgba(0,0,0,0.4)',
      }}
    >
      <div className="h-full overflow-hidden">{children}</div>
    </div>
  )
}

function BackButton({ onClick }) {
  return (
    <button
      onClick={onClick}
      className="flex items-center gap-2 text-sm text-gray-400 hover:text-white transition-colors bg-gray-900/60 hover:bg-gray-800 px-3 py-1.5 rounded-lg border border-gray-800"
    >
      <ArrowLeft size={14} /> Back to Hub
    </button>
  )
}

export default function App() {
  const [role, setRole] = useState(null)
  const [showArchitecture, setShowArchitecture] = useState(false)
  const [resetting, setResetting] = useState(false)
  const [resetSuccess, setResetSuccess] = useState(false)

  const handleResetDemo = async () => {
    try {
      setResetting(true)
      await api.resetDemo()
      setResetSuccess(true)
      setTimeout(() => setResetSuccess(false), 3000)
    } catch (e) {
      console.error('Demo reset error:', e)
    } finally {
      setResetting(false)
    }
  }

  if (role === 'victim') {
    return (
      <div className="min-h-screen bg-[#06080F] flex flex-col items-center justify-center gap-4 p-4">
        <div className="w-full max-w-[390px] flex justify-between items-center">
          <BackButton onClick={() => setRole(null)} />
          <span className="text-[11px] font-mono text-critical uppercase font-bold tracking-wider">
            Offline SOS Sim
          </span>
        </div>
        <PhoneFrame><VictimApp /></PhoneFrame>
        <p className="text-xs text-gray-500 font-mono tracking-wide">
          EDGE RESCUE · ON-DEVICE MULTIMODAL TRIAGE
        </p>
      </div>
    )
  }

  if (role === 'responder') {
    return (
      <div className="min-h-screen bg-[#06080F] flex flex-col items-center justify-center gap-4 p-4">
        <div className="w-full max-w-[390px] flex justify-between items-center">
          <BackButton onClick={() => setRole(null)} />
          <span className="text-[11px] font-mono text-relay uppercase font-bold tracking-wider">
            Tactical Unit
          </span>
        </div>
        <PhoneFrame><ResponderApp /></PhoneFrame>
        <p className="text-xs text-gray-500 font-mono tracking-wide">
          EDGE RESCUE · RESPONDER FIELD APP (R-114)
        </p>
      </div>
    )
  }

  if (role === 'supervisor') {
    return (
      <div className="min-h-screen bg-[#06080F] flex flex-col supervisor-theme text-white">
        <div className="px-6 pt-3 pb-1 flex justify-between items-center border-b border-gray-900 bg-[#06080F]">
          <BackButton onClick={() => setRole(null)} />
          <div className="flex items-center gap-3">
            <span className="text-xs text-gray-400 font-mono hidden sm:inline">
              Command & Control Tactical Interface
            </span>
            <button
              onClick={handleResetDemo}
              disabled={resetting}
              className="flex items-center gap-1.5 text-xs font-mono text-gray-400 hover:text-white bg-gray-900 px-2.5 py-1 rounded border border-gray-800 transition-colors"
            >
              <RotateCcw size={12} className={resetting ? 'animate-spin' : ''} />
              {resetSuccess ? 'Reset Complete!' : 'Reset Demo'}
            </button>
          </div>
        </div>
        <SupervisorApp />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#06080F] text-white flex flex-col justify-between px-4 sm:px-6 py-8">
      {/* Top bar */}
      <header className="max-w-6xl w-full mx-auto flex items-center justify-between pb-6 border-b border-gray-900/60">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-red-500 to-amber-500 flex items-center justify-center shadow-lg shadow-red-500/20">
            <Radio size={18} className="text-white" />
          </div>
          <div>
            <span className="font-extrabold text-sm tracking-wider uppercase text-white">
              EDGE RESCUE
            </span>
            <span className="hidden sm:inline-block ml-2 px-2 py-0.5 rounded-full text-[10px] font-mono bg-relay/10 text-relay border border-relay/30">
              v1.0 Submission State
            </span>
          </div>
        </div>

        <div className="flex items-center gap-2 sm:gap-3">
          <button
            onClick={() => setShowArchitecture((prev) => !prev)}
            className="flex items-center gap-1.5 text-xs text-gray-300 hover:text-white bg-gray-900/80 hover:bg-gray-800 px-3 py-1.5 rounded-lg border border-gray-800 transition-colors"
          >
            <Info size={14} className="text-relay" />
            <span className="hidden sm:inline">How It Works</span>
            <span className="sm:hidden">Info</span>
          </button>
          <button
            onClick={handleResetDemo}
            disabled={resetting}
            className="flex items-center gap-1.5 text-xs text-gray-400 hover:text-white bg-gray-900/80 hover:bg-gray-800 px-3 py-1.5 rounded-lg border border-gray-800 transition-colors"
            title="Clear all active packets & assignments for a fresh demo"
          >
            <RotateCcw size={13} className={resetting ? 'animate-spin' : ''} />
            <span className="hidden sm:inline">{resetSuccess ? 'Reset!' : 'Reset Demo'}</span>
          </button>
        </div>
      </header>

      {/* Hero section */}
      <main className="max-w-4xl w-full mx-auto text-center my-auto py-8">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-500/10 border border-red-500/20 text-red-400 text-xs font-mono uppercase tracking-widest mb-6">
          <WifiOff size={13} />
          <span>When the towers fall, the response does not.</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-black text-white tracking-tight mb-4">
          EDGE RESCUE
        </h1>

        <p className="text-lg sm:text-2xl font-light text-gray-300 mb-3 tracking-wide">
          Autonomous AI for a World Without Internet
        </p>

        <p className="text-sm text-gray-500 max-w-2xl mx-auto mb-10 leading-relaxed font-sans">
          Two-tier edge intelligence: on-device multimodal AI triages in any native language with zero connectivity,
          relayed over Bluetooth GATT through drones to an autonomous coordinator that assigns responders in real time.
        </p>

        {/* 3 Role Selection Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full text-left">
          {[
            {
              id: 'victim',
              label: 'Victim SOS Simulator',
              badge: 'Edge Node · Offline',
              sub: 'Send multimodal SOS: voice notes, photos, GPS. On-device LiteRT triage and BLE GATT broadcast.',
              Icon: BellRing,
              iconColor: 'text-red-400',
              iconBg: 'bg-red-500/10 group-hover:bg-red-500/20',
              border: 'hover:border-red-500/40 hover:shadow-red-500/10',
            },
            {
              id: 'responder',
              label: 'Field Responder',
              badge: 'Tactical Unit · R-114',
              sub: 'Field-optimized tactical dashboard: prioritized triage queue, distance metrics, mesh status & telemetry.',
              Icon: ShieldCheck,
              iconColor: 'text-relay',
              iconBg: 'bg-relay/10 group-hover:bg-relay/20',
              border: 'hover:border-relay/50 hover:shadow-cyan-500/10',
            },
            {
              id: 'supervisor',
              label: 'Command Supervisor',
              badge: 'Central Hub · Ops',
              sub: 'Tactical command center: real-time map, multi-factor AI assignment, live unit tracking & team dispatch.',
              Icon: Monitor,
              iconColor: 'text-purple-400',
              iconBg: 'bg-purple-500/10 group-hover:bg-purple-500/20',
              border: 'hover:border-purple-500/40 hover:shadow-purple-500/10',
            },
          ].map(({ id, label, badge, sub, Icon, iconColor, iconBg, border }) => (
            <button
              key={id}
              onClick={() => setRole(id)}
              className={`p-6 rounded-2xl border border-gray-800/80 bg-[#0A0E14] transition-all duration-200 group flex flex-col justify-between shadow-xl ${border}`}
            >
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div className={`w-12 h-12 rounded-xl flex items-center justify-center transition-colors ${iconBg}`}>
                    <Icon size={24} className={iconColor} />
                  </div>
                  <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-gray-900 border border-gray-800 text-gray-400">
                    {badge}
                  </span>
                </div>
                <h2 className="text-white font-bold text-lg mb-1.5 flex items-center gap-1.5">
                  {label}
                  <ChevronRight size={16} className="text-gray-600 group-hover:text-white transition-transform group-hover:translate-x-1" />
                </h2>
                <p className="text-gray-400 text-xs leading-relaxed">{sub}</p>
              </div>

              <div className="mt-5 pt-3 border-t border-gray-900 flex items-center justify-between text-[11px] font-mono text-gray-500">
                <span>Launch interface</span>
                <span className="text-relay">→</span>
              </div>
            </button>
          ))}
        </div>

        {/* Architecture & Offline Resilience Drawer */}
        {showArchitecture && (
          <div className="mt-10 text-left bg-[#0A0E14] border border-gray-800 rounded-2xl p-6 sm:p-8 animate-in fade-in duration-300">
            <div className="flex items-center justify-between pb-4 border-b border-gray-800">
              <div className="flex items-center gap-2.5">
                <Layers className="text-relay" size={20} />
                <h2 className="text-lg font-bold text-white">System Architecture & Offline Resilience</h2>
              </div>
              <button
                onClick={() => setShowArchitecture(false)}
                className="text-gray-400 hover:text-white text-xs font-mono"
              >
                Close ✕
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mt-6">
              <div className="bg-black/30 border border-gray-800/60 rounded-xl p-4">
                <span className="text-xs font-mono text-red-400 font-bold">01 · Why Offline First?</span>
                <h3 className="text-sm font-semibold text-white mt-1">Infrastructure Collapse</h3>
                <p className="text-xs text-gray-400 mt-2 leading-relaxed">
                  In Kerala 2018 or Cyclone Fani, cell towers and power fail first. Standard cloud APIs (GPT-4, Claude) are completely inaccessible. Edge Rescue runs local.
                </p>
              </div>

              <div className="bg-black/30 border border-gray-800/60 rounded-xl p-4">
                <span className="text-xs font-mono text-amber-400 font-bold">02 · Multimodal Edge AI</span>
                <h3 className="text-sm font-semibold text-white mt-1">Gemma 4 E2B on Phone</h3>
                <p className="text-xs text-gray-400 mt-2 leading-relaxed">
                  Runs via LiteRT on device without internet. Understands Telugu/Hindi/Malayalam audio and flood/fire photos to generate a structured English triage packet.
                </p>
              </div>

              <div className="bg-black/30 border border-gray-800/60 rounded-xl p-4">
                <span className="text-xs font-mono text-relay font-bold">03 · BLE Drone Relay</span>
                <h3 className="text-sm font-semibold text-white mt-1">GATT Server & ACK</h3>
                <p className="text-xs text-gray-400 mt-2 leading-relaxed">
                  The victim phone acts as a Bluetooth GATT server (MTU 512). Search drones read the rich JSON packet over BLE, relay to hub, and write back an instant confirmation ACK.
                </p>
              </div>

              <div className="bg-black/30 border border-gray-800/60 rounded-xl p-4">
                <span className="text-xs font-mono text-purple-400 font-bold">04 · Autonomous Hub</span>
                <h3 className="text-sm font-semibold text-white mt-1">Scoring & Team Dispatch</h3>
                <p className="text-xs text-gray-400 mt-2 leading-relaxed">
                  Algorithmic multi-factor ranking (skills, equipment, distance, battery) paired with Gemma 4 26B context judgment and automatic dual-role team deployment.
                </p>
              </div>
            </div>

            <div className="mt-6 p-4 rounded-xl bg-relay/5 border border-relay/20 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 text-xs">
              <div className="flex items-center gap-2 text-relay font-medium">
                <CheckCircle2 size={16} />
                <span>Zero-Crash Offline Guarantee: Rule-based fallbacks keep dispatch 100% operational even without API keys or internet.</span>
              </div>
              <span className="font-mono text-gray-400 text-[11px]">PostgreSQL 16 · Redis 7 · LiteRT</span>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="max-w-4xl w-full mx-auto pt-6 border-t border-gray-900/60 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-gray-600 font-mono">
        <div>
          <span>EDGE RESCUE</span>
          <span className="mx-2">·</span>
          <span>AUTONOMOUS DISASTER RESPONSE</span>
        </div>
        <div className="tracking-wider">
          TWO-TIER GEMMA 4 · BLE GATT RELAY · OFFLINE FIRST
        </div>
      </footer>
    </div>
  )
}

