import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  const body = await request.json()
  const query = body.query
  
  // Here you would typically call your actual search API
  const result = `Here's what I found about Akhilesh related to "${query}"`

  return NextResponse.json({ result })
}