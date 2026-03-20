import { ImageResponse } from "next/og";

export const runtime = "edge";
export const alt = "Shippage — Ship a landing page from your terminal";
export const size = { width: 1200, height: 630 };
export const contentType = "image/png";

export default async function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          width: "100%",
          height: "100%",
          backgroundColor: "#0a0a0a",
          color: "#fafafa",
          padding: "60px",
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: "12px",
            marginBottom: "24px",
          }}
        >
          <div
            style={{
              width: "48px",
              height: "48px",
              borderRadius: "8px",
              backgroundColor: "#6366f1",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              fontSize: "24px",
            }}
          >
            &gt;_
          </div>
          <span style={{ fontSize: "36px", fontWeight: "bold" }}>Shippage</span>
        </div>
        <h1
          style={{
            fontSize: "56px",
            fontWeight: "bold",
            textAlign: "center",
            lineHeight: 1.2,
            maxWidth: "800px",
          }}
        >
          Ship a landing page from your terminal.
        </h1>
        <p
          style={{
            fontSize: "24px",
            color: "#a1a1aa",
            marginTop: "16px",
            textAlign: "center",
          }}
        >
          One sentence. Production-ready page. No AI slop. Free forever.
        </p>
        <div
          style={{
            display: "flex",
            gap: "16px",
            marginTop: "32px",
            fontSize: "18px",
            color: "#6366f1",
          }}
        >
          <span>18 sections</span>
          <span style={{ color: "#404040" }}>·</span>
          <span>200+ design tokens</span>
          <span style={{ color: "#404040" }}>·</span>
          <span>6 frameworks</span>
        </div>
      </div>
    ),
    { ...size },
  );
}
