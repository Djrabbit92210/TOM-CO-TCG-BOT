/** Simulated API latency for UI realism (no real backend). */
export function apiDelay(ms = 280) {
  return new Promise((r) => setTimeout(r, ms))
}

export async function mockSave<T>(payload: T): Promise<{ ok: true; data: T }> {
  await apiDelay()
  return { ok: true, data: payload }
}
