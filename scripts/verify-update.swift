import Foundation
import CryptoKit
let key = try Curve25519.Signing.PublicKey(rawRepresentation: Data(base64Encoded: CommandLine.arguments[1])!)
let signature = Data(base64Encoded: CommandLine.arguments[2])!
let data = try Data(contentsOf: URL(fileURLWithPath: CommandLine.arguments[3]))
assert(key.isValidSignature(signature, for: data), "Archive signature invalid")
assert(!key.isValidSignature(signature, for: data + Data("tamper-test".utf8)), "Tampered archive accepted")
print("PASS: signed archive accepted, tampered archive rejected")
