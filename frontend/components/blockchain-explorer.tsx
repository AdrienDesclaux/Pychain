"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Badge } from "@/components/ui/badge"
import { Separator } from "@/components/ui/separator"
import { useToast } from "@/hooks/use-toast"
import { Loader2, Box, Send, Pickaxe, Wallet, Shield } from "lucide-react"

interface Transaction {
  sender: string
  recipient: string
  amount: number
}

interface Block {
  hash: string
  previous_hash: string
  timestamp: number
  nonce: number
  transactions: Transaction[]
}

const API_BASE = "http://localhost:5000"

export default function BlockchainExplorer() {
  const [chain, setChain] = useState<Block[]>([])
  const [loading, setLoading] = useState(true)
  const [mining, setMining] = useState(false)
  const [validating, setValidating] = useState(false)
  const [balanceLoading, setBalanceLoading] = useState(false)
  const [transactionLoading, setTransactionLoading] = useState(false)

  const [sender, setSender] = useState("")
  const [recipient, setRecipient] = useState("")
  const [amount, setAmount] = useState("")
  const [balanceAddress, setBalanceAddress] = useState("")
  const [balance, setBalance] = useState<number | null>(null)

  const { toast } = useToast()

  const fetchChain = async () => {
    try {
      const response = await fetch(`${API_BASE}/chain`)
      if (!response.ok) throw new Error("Failed to fetch chain")
      const data = await response.json()
      console.log(data)
      setChain(data || [])
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to fetch blockchain data",
        variant: "destructive",
      })
    } finally {
      setLoading(false)
    }
  }

  const sendTransaction = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!sender || !recipient || !amount) return

    setTransactionLoading(true)
    try {
      const response = await fetch(`${API_BASE}/transaction`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sender,
          recipient,
          amount: Number.parseFloat(amount),
        }),
      })

      if (!response.ok) throw new Error("Transaction failed")

      toast({
        title: "Success",
        description: "Transaction added to mempool",
      })

      setSender("")
      setRecipient("")
      setAmount("")
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to send transaction",
        variant: "destructive",
      })
    } finally {
      setTransactionLoading(false)
    }
  }

  const mineBlock = async () => {
    setMining(true)
    try {
      const response = await fetch(`${API_BASE}/mine`, { method: "POST" })
      if (!response.ok) throw new Error("Mining failed")

      toast({
        title: "Success",
        description: "Block mined successfully!",
      })

      await fetchChain()
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to mine block",
        variant: "destructive",
      })
    } finally {
      setMining(false)
    }
  }

  const checkBalance = async () => {
    if (!balanceAddress) return

    setBalanceLoading(true)
    try {
      const response = await fetch(`${API_BASE}/balance/${balanceAddress}`)
      if (!response.ok) throw new Error("Failed to check balance")

      const data = await response.json()
      setBalance(data.balance)
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to check balance",
        variant: "destructive",
      })
    } finally {
      setBalanceLoading(false)
    }
  }

  const validateChain = async () => {
    setValidating(true)
    try {
      const response = await fetch(`${API_BASE}/validate`)
      if (!response.ok) throw new Error("Validation failed")

      const data = await response.json()
      toast({
        title: data.valid ? "Valid Chain" : "Invalid Chain",
        description: data.valid ? "Blockchain is valid" : "Blockchain integrity compromised",
        variant: data.valid ? "default" : "destructive",
      })
    } catch (error) {
      toast({
        title: "Error",
        description: "Failed to validate chain",
        variant: "destructive",
      })
    } finally {
      setValidating(false)
    }
  }

  const formatTimestamp = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleString()
  }

  const truncateHash = (hash: string) => {
    return `${hash.slice(0, 8)}...${hash.slice(-8)}`
  }

  useEffect(() => {
    fetchChain()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-blue-500" />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 flex items-center gap-3">
            <Box className="h-10 w-10 text-blue-500" />
            Blockchain Explorer
          </h1>
          <p className="text-gray-400">Explore blocks, transactions, and manage your blockchain</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
          {/* Transaction Form */}
          <Card className="bg-gray-800 border-gray-700">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Send className="h-5 w-5 text-green-500" />
                Send Transaction
              </CardTitle>
            </CardHeader>
            <CardContent>
              <form onSubmit={sendTransaction} className="space-y-4">
                <div>
                  <Label htmlFor="sender">Sender</Label>
                  <Input
                    id="sender"
                    value={sender}
                    onChange={(e) => setSender(e.target.value)}
                    placeholder="Sender address"
                    className="bg-gray-700 border-gray-600"
                  />
                </div>
                <div>
                  <Label htmlFor="recipient">Recipient</Label>
                  <Input
                    id="recipient"
                    value={recipient}
                    onChange={(e) => setRecipient(e.target.value)}
                    placeholder="Recipient address"
                    className="bg-gray-700 border-gray-600"
                  />
                </div>
                <div>
                  <Label htmlFor="amount">Amount</Label>
                  <Input
                    id="amount"
                    type="number"
                    step="0.01"
                    value={amount}
                    onChange={(e) => setAmount(e.target.value)}
                    placeholder="0.00"
                    className="bg-gray-700 border-gray-600"
                  />
                </div>
                <Button type="submit" className="w-full bg-green-600 hover:bg-green-700" disabled={transactionLoading}>
                  {transactionLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : "Send Transaction"}
                </Button>
              </form>
            </CardContent>
          </Card>

          {/* Balance Checker */}
          <Card className="bg-gray-800 border-gray-700">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Wallet className="h-5 w-5 text-yellow-500" />
                Check Balance
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <Label htmlFor="balance-address">Address</Label>
                <Input
                  id="balance-address"
                  value={balanceAddress}
                  onChange={(e) => setBalanceAddress(e.target.value)}
                  placeholder="Enter address"
                  className="bg-gray-700 border-gray-600"
                />
              </div>
              <Button
                onClick={checkBalance}
                className="w-full bg-yellow-600 hover:bg-yellow-700"
                disabled={balanceLoading}
              >
                {balanceLoading ? <Loader2 className="h-4 w-4 animate-spin" /> : "Check Balance"}
              </Button>
              {balance !== null && (
                <div className="text-center p-3 bg-gray-700 rounded">
                  <p className="text-sm text-gray-400">Balance</p>
                  <p className="text-2xl font-bold text-yellow-400">{balance}</p>
                </div>
              )}
            </CardContent>
          </Card>

          {/* Actions */}
          <Card className="bg-gray-800 border-gray-700">
            <CardHeader>
              <CardTitle>Actions</CardTitle>
            </CardHeader>
            <CardContent className="space-y-3">
              <Button onClick={mineBlock} className="w-full bg-orange-600 hover:bg-orange-700" disabled={mining}>
                {mining ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin mr-2" />
                    Mining...
                  </>
                ) : (
                  <>
                    <Pickaxe className="h-4 w-4 mr-2" />
                    Mine Block
                  </>
                )}
              </Button>
              <Button
                onClick={validateChain}
                variant="outline"
                className="w-full border-gray-600 hover:bg-gray-700 bg-transparent"
                disabled={validating}
              >
                {validating ? (
                  <>
                    <Loader2 className="h-4 w-4 animate-spin mr-2" />
                    Validating...
                  </>
                ) : (
                  <>
                    <Shield className="h-4 w-4 mr-2" />
                    Validate Chain
                  </>
                )}
              </Button>
              <Button
                onClick={fetchChain}
                variant="outline"
                className="w-full border-gray-600 hover:bg-gray-700 bg-transparent"
              >
                Refresh Chain
              </Button>
            </CardContent>
          </Card>
        </div>

        {/* Blockchain Display */}
        <Card className="bg-gray-800 border-gray-700 md:mb-16 mb-16">
          <CardHeader>
            <CardTitle>Blockchain ({chain.length} blocks)</CardTitle>
            <CardDescription>Latest blocks in descending order</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {chain
                .slice()
                .reverse()
                .map((block, index) => (
                  <div key={block.hash} className="border border-gray-700 rounded-lg p-4">
                    <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-3">
                      <Badge variant="outline" className="w-fit mb-2 sm:mb-0">
                        Block #{chain.length - index}
                      </Badge>
                      <span className="text-sm text-gray-400">{formatTimestamp(block.timestamp)}</span>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-gray-400">Hash:</p>
                        <p className="font-mono text-blue-400 break-all">{truncateHash(block.hash)}</p>
                      </div>
                      <div>
                        <p className="text-gray-400">Previous Hash:</p>
                        <p className="font-mono text-purple-400 break-all">{truncateHash(block.previous_hash)}</p>
                      </div>
                      <div>
                        <p className="text-gray-400">Nonce:</p>
                        <p className="font-mono">{block.nonce}</p>
                      </div>
                      <div>
                        <p className="text-gray-400">Transactions:</p>
                        <p className="font-mono">{block.transactions.length}</p>
                      </div>
                    </div>

                    {block.transactions.length > 0 && (
                      <>
                        <Separator className="my-3 bg-gray-700" />
                        <div>
                          <p className="text-gray-400 mb-2">Transactions:</p>
                          <div className="space-y-2">
                            {block.transactions.map((tx, txIndex) => (
                              <div key={txIndex} className="bg-gray-700 p-2 rounded text-xs">
                                <span className="text-green-400">{truncateHash(tx.sender)}</span>
                                <span className="text-gray-400 mx-2">→</span>
                                <span className="text-blue-400">{truncateHash(tx.recipient)}</span>
                                <span className="text-gray-400 mx-2">:</span>
                                <span className="text-yellow-400 font-bold">{tx.amount}</span>
                              </div>
                            ))}
                          </div>
                        </div>
                      </>
                    )}
                  </div>
                ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
