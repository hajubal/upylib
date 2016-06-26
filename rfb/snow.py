import rfb, os

class Snow(rfb.RfbSession):

    def __init__(self, conn, w, h, colourmap, name):
        super().__init__(conn, w, h, colourmap, name)
        self.snowflakes = []
    
    def update(self):

        for idx, flake in enumerate(self.snowflakes):
            # destroy any RawRect snowflakes
            if type(flake) is rfb.RawRect:
                del( self.snowflakes[idx] )
            # move any CopyRect snowflakes
            if type(flake) is rfb.CopyRect:
                if flake.y + flake.h + flake.vector >= 255:
                    del( self.snowflakes[idx] )
                else:
                    flake.y += flake.vector 

        # create new snowflakes
        for i in range( os.urandom(1)[0]%20 ):
            x = os.urandom(2)[0]
            x = x if x<self.w-4 else x-4
            y = 0
            w = h = os.urandom(1)[0]%3+1
            vector = 4-w
            self.snowflakes.append(
                rfb.RawRect(
                    x, y,
                    w, h,
                    self.bpp, self.depth, self.true,
                    self.colourmap, self.shift
                )
            )
            self.snowflakes[-1].fill((255,255,255))
            self.snowflakes[-1].vector = vector            
            self.snowflakes.append(
                rfb.CopyRect(
                    x, y,
                    w, h,
                    0, vector
                )
            )
            # add vector property
            self.snowflakes[-1].vector = vector            

        self.send( rfb.ServerFrameBufferUpdate( self.snowflakes ))


svr = rfb.RfbServer(255, 255, name=b'snow', handler=Snow)
svr.serve()