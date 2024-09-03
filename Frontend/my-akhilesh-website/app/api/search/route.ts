import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  const body = await request.json()
  const prompt = body.query

  try {
    const response = await fetch(`https://llmyoubackend-production.up.railway.app/generate_response?prompt=${encodeURIComponent(prompt)}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    if (!response.ok) {
      throw new Error(`Failed to fetch response from API: ${response.status} ${response.statusText}`)
    }

    const data = await response.json()
    return NextResponse.json({ result: data.response })
  } catch (error) {
    console.error('Error fetching response:', error)
    return NextResponse.json({ error: 'Failed to generate response' }, { status: 500 })
  }
}