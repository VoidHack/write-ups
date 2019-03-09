import sys
import random
import struct
from hashlib import md5

p_8  = lambda val : struct.pack( "!B", val )
p_16 = lambda val : struct.pack( "!H", val )
p_32 = lambda val : struct.pack( "!L", val )

u_8  = lambda val : struct.unpack( "!B", val )[ 0 ]
u_16 = lambda val : struct.unpack( "!H", val )[ 0 ]
u_32 = lambda val : struct.unpack( "!L", val )[ 0 ]

class Crc:
	m_poly = 0x1021
	m_initial = 0xffff
	m_table = None

	def __init__( self, initial = 0, poly = 0 ):
		if initial:
			self.m_initial = initial

		if poly:
			self.m_poly = poly

		self.genTable()

	def intialVal( self, byte ):
		crc = 0
		byte = byte << 8
		
		for j in range( 8 ):
		
			if (crc ^ byte) & 0x8000:
				crc = (crc << 1) ^ self.m_poly
			else:
				crc = crc << 1
		
			byte = byte << 1

		return crc

	def genTable( self ):
		self.m_table = [ self.intialVal( i ) for i in range( 256 ) ]

	def update( self, crc, byte ):
		cc = 0xff & byte

		tmp = ( crc >> 8 ) ^ cc
		crc = ( crc << 8 ) ^ self.m_table[ tmp & 0xff ]
		crc = crc & 0xffff
	
		return crc

	def crc( self, buf ):
		crc = self.m_initial

		for c in buf:
			crc = self.update( crc, ord( c ) )

		return crc

	def __call__( self, buf ):
		return self.crc( buf )

class Key:
	m_key = None
	m_pad = 0x00

	def __init__( self, key ):
		self.m_key = key

		if not self.checkKeyLen():
			self.expandKey()

	def checkKeyLen( self ):
		return len( self.m_key ) == 32

	def expandKey( self ):
		if len( self.m_key ) < 32:
			countOfBytes = 32 - len( self.m_key )
			self.m_key += p_8( self.m_pad ) * countOfBytes

		return True

	def getKey( self ):
		return self.m_key

class Cipher:
	m_table = []
	m_buf = ''
	m_blocks = []
	m_key = None
	m_encFileName = ''

	def __init__( self, buf, key, filename ):
		self.m_buf = buf
		self.m_key = key	
		self.m_encFileName = filename + ".enc"

		self.initTable()

	def initTable( self ):
		seed = self.m_key.getKey()
		seed = u_32( seed[:4] )

		random.seed( seed )

		for i in range( 32 ):
			self.m_table.append( random.randint( 0, 255 ) )

	def viewTable( self ):
		print self.m_table

	def parseData( self ):
		i = 0

		while i < len( self.m_buf ):
			self.m_blocks.append( self.m_buf[ i : i + 32 ] )
			i += 32

		for i in range( len( self.m_blocks ) ):
			if len( self.m_blocks[ i ] ) != 32:
				padding = 32 - len( self.m_blocks[ i ] )
				self.m_blocks[ i ] += p_8( 0x0 ) * padding

	def getGamma( self, block ):
		gamma = ''

		crc = Crc()
		block_crc = p_16( crc( block ) )

		for i in range( 16 ):
			val = ord( block_crc[ i % 2 ] )
			val >>= 1 
			val ^= ord( self.m_key.getKey()[ i ] )
			val &= 0xff

			gamma += chr( val )

		return gamma

	def writeBlock2File( self, block ):
		fd = open( self.m_encFileName, 'ab' )
		fd.write( block )
		fd.close()

	def encode( self ):
		self.parseData()

		for i in range( len( self.m_blocks ) ):
			enc_block = ''
			block = self.m_blocks[ i ]
			gamma = self.getGamma( block[:16] )
			crc = Crc()( block )

			for j in range( len( gamma ) ):
				enc_block += chr( ord( block[ j ] ) ^ ord( gamma[ j ] ) )

			gamma = self.getGamma( block[16:] )

			for j in range( 16, len( block ) ):
				enc_block += chr( ord( block[ j ] ) ^ ord( gamma[ j % 16 ] ) )

			enc_block += p_16( crc )

			self.writeBlock2File( enc_block )

	def decode( self ):
		'''oooops.....'''

def GetFileData( filename ):
	fd = None

	try:
		fd = open( filename, 'rb' )
	except:
		print "[-] Error in file open!"
		sys.exit( -2 )

	buf = ''
	buf = fd.read()

	fd.close()

	if buf == '':
		print "File is empty!"
		sys.exit( -3 )
	else:
		return buf

def checkKeySymbols( key ):
	for i in key:
		if i not in "01234567890abcdef":
			return True

	return False

if __name__ == "__main__":

	if len( sys.argv ) > 2:
		filename = sys.argv[ 1 ]
		key	  = sys.argv[ 2 ]
	else:
		print "Usage python " + sys.argv[ 0 ] + " <filename> <key>"
		sys.exit( -1 )

	key = md5( key ).hexdigest()

	if len( key ) != 32:
		print "[-] Error key len!"
		sys.exit( -1337 )

	if checkKeySymbols( key ):
		print "[-] Error key symbols!"
		sys.exit( -31337 )

	fileData = GetFileData( filename )

	key = Key( key )
	cipher = Cipher( fileData, key, filename )

	cipher.encode()