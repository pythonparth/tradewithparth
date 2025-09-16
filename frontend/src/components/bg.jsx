import chartLogo from '../assets/stock-movement-svgrepo-com.svg'

export default function Background(){
    return(
        <div style={{
                position: 'fixed',
                top: 0,
                left: 0,
                width: '100vw',
                height: '100vh',
                zIndex: 0,
                overflow: 'hidden',
                pointerEvents: 'none',
              }}>
                <img
                  src={chartLogo}
                  alt="Stock Movement"
                  style={{
                    position: 'absolute',
                    left: 0,
                    top: 0,
                    width: '100vw',
                    height: '100vh',
                    objectFit: 'cover',
                    opacity: 0.08,
                    filter: 'blur(1px) drop-shadow(0 0 2em #00e67688)',
                    zIndex: 0,
                    pointerEvents: 'none',
                  }}
                />
        </div>
    )
}